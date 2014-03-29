'''
Created on Mar 14, 2014

@author: Tuan
'''
from bisect import bisect_left
import codecs
from collections import defaultdict
import json
import pickle

from brandeis.bigdata.wiki.data_controller.tree_data import Tree_Data
from brandeis.bigdata.wiki.language_utils.named_entity import IncorrectIndexException
from brandeis.bigdata.wiki.language_utils.named_entity import Named_Entity
from brandeis.bigdata.wiki.utils.constant import *


class Node_Indexer(object):
    def __init__(self, node_data, node_supercategories):
        '''
        Wrap a Node_Data type object node_data
        Decorate it with indexing method
        '''
        self.node_data = node_data
        self.node_supercategories = node_supercategories
        
        self.node_value = {}
        if CM_TITLE in self.node_data._node_params:
            self.node_value[CM_TITLE] = self.node_data._node_params[CM_TITLE]
        if CM_PAGEID in self.node_data._node_params:
            self.node_value[CM_PAGEID] = self.node_data._node_params[CM_PAGEID]
        
    def index(self):
        try:
            for page in self.node_data.pages:
                Tree_Ancestor_Indexer.index[SUBKEY_PAGE][page[SUBKEY_TITLE]] = \
                     Tree_Ancestor_Indexer.index[SUBKEY_PAGE][page[SUBKEY_TITLE]].\
                     union(self.node_supercategories).\
                     union(set([self.node_value[CM_TITLE]]))
        except AttributeError:
            pass
        try:
            for sub_node in self.node_data.sub_nodes:
                Tree_Ancestor_Indexer.index[SUBKEY_SUBCAT][sub_node._node_params[CM_TITLE]] = \
                         Tree_Ancestor_Indexer.index[SUBKEY_SUBCAT][sub_node._node_params[CM_TITLE]].\
                         union(self.node_supercategories).union(set([self.node_value[CM_TITLE]]))
                subcat_indexer = Node_Indexer(sub_node,
                                              Tree_Ancestor_Indexer.index[SUBKEY_SUBCAT][sub_node._node_params[CM_TITLE]])
                subcat_indexer.index()
        except AttributeError:
            pass

PRINT_MAX = 1000
class Tree_Ancestor_Indexer(object):
    '''
    Index the hierarchical structure into an indexing of the following format:
    Dict[(person_name, person_id)] = [list of profession categories]
    '''
    def __init__(self):
        '''
        Tree_Ancestor_Indexer.index keep the index of the whole hierarchy
        '''
        Tree_Ancestor_Indexer.index = {SUBKEY_SUBCAT: defaultdict(set),
                              SUBKEY_PAGE: defaultdict(set)}
        Named_Entity.Profession_Name_Entity.loadNationality();
        self.number_of_people = 0
        self.number_of_profession = 0
        self.flat_index = {}
        self.profession_histogram = defaultdict(int)
        
    def initiate_from_file(self, file_name):
        
        '''
        Input file must be a data file saved using tree data class
        '''
        print "=============INITIATE FROM FILE=============="
        self.tree = Tree_Data.load_from_file(file_name)
        
    def run_index(self, filter_function=lambda x: x):
        print "=============RUN INDEXING=============="
        root_indexer = Node_Indexer(self.tree.root, [])
#         root_indexer = Node_Indexer(self.tree.root, set())
        root_indexer.index()
        
        
        self.number_of_pages = len(Tree_Ancestor_Indexer.index[SUBKEY_PAGE])
        print self.number_of_pages
        self.number_of_subcats = len(Tree_Ancestor_Indexer.index[SUBKEY_SUBCAT])
        print self.number_of_subcats
        
    def post_process_indexing_filter_profession(self):
        print "=============FILTER PROFESSION=============="
        for key in Tree_Ancestor_Indexer.index[SUBKEY_PAGE]:
            try:
                professions = set()
                correct_index = True
                for string in Tree_Ancestor_Indexer.index[SUBKEY_PAGE][key]:
                    try:
                        profession = Named_Entity.Profession_Name_Entity.professionCategoryTransform(string)
                        if profession != None and profession != '':
                            professions.add(profession)
                    except IncorrectIndexException:
                        correct_index = False
                        break
                if correct_index:
                    professions = list(professions)
                    for profession in professions:
                        self.profession_histogram[profession] += 1
                    self.number_of_people += 1 
                    self.flat_index[key] = professions
            except UnicodeEncodeError:
                pass
        self.number_of_profession = len(self.profession_histogram)
        self.print_statistics()
    
    def print_statistics(self):
        print 'Number of people after filter profession %d' % self.number_of_people
        print 'Number of profession after filter profession %d' % self.number_of_profession
        
    def save_profession_histogram(self, file_name):
        print "=============SAVE HISTOGRAM=============="
        with codecs.open(file_name, 'w', 'utf-8') as file_handler:
            json.dump(self.profession_histogram , file_handler)
    
    def load_profession_histogram(self, file_name):
        print "=============LOAD HISTOGRAM=============="
        with codecs.open(file_name, 'r', 'utf-8') as file_handler:
            self.profession_histogram = json.load(file_handler)
    
    def save_flat_index(self, file_name):
        print "=============SAVE FLAT INDEX=============="
        with codecs.open(file_name, 'w', 'utf-8') as file_handler:
            json.dump(self.flat_index , file_handler)
    
    def load_flat_index(self, file_name):
        print "=============LOAD FLAT INDEX=============="
        with codecs.open(file_name, 'r', 'utf-8') as file_handler:
            self.flat_index = json.load(file_handler)
            
    def post_process_indexing_statistic(self, LOW_THRESHOLD):
        print "=============STATISTICS=============="
        new_profession_histogram = {}
        for profession in self.profession_histogram:
            if self.profession_histogram[profession] < LOW_THRESHOLD:
                pass
            else:
                new_profession_histogram[profession] = self.profession_histogram[profession] 
        
        self.profession_histogram = new_profession_histogram
        
        profession_names = self.profession_histogram.keys()
        profession_names.sort()
        print profession_names
        
        self.number_of_people = len(self.flat_index.keys())
        self.number_of_profession = len(profession_names)
        self.print_statistics()
        
        self.number_of_people = 0
        self.new_flat_index = {}
        for key in self.flat_index:
            new_profession_list = []
            for profession in self.flat_index[key]:
                index = bisect_left(profession_names, profession)
                if index < len(profession_names):
                    if profession_names[index] == profession:
                        new_profession_list.append(profession)
            if len(new_profession_list) != 0:
                self.number_of_people += 1
                if self.number_of_people % 100 == 0:
                    print self.number_of_people
                self.new_flat_index[key] = new_profession_list
                
        self.flat_index = self.new_flat_index
        self.print_statistics()
                
    def print_readable_to_file(self, file_name):
        with codecs.open(file_name, 'w', 'utf-8') as file_handler:
            for key in self.flat_index:
                try:
                    file_handler.write(key + ' ' + str(self.flat_index[key]) + '\n')
                except UnicodeEncodeError:
                    pass
                
    def save_to_file(self, file_name):
        with open(file_name, 'w') as write_file:
            pickle.dump(Tree_Ancestor_Indexer.index, write_file)
    
    @classmethod
    def load_from_file(cls, file_name):
        with open(file_name, 'r') as read_file:
            Tree_Ancestor_Indexer.index = pickle.load(read_file)
