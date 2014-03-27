'''
Created on Mar 14, 2014

@author: Tuan
'''
import pickle
from collections import defaultdict
from brandeis.bigdata.wiki.data_controller.tree_data import Tree_Data
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
                Tree_Ancestor_Indexer.index[SUBKEY_PAGE][page[SUBKEY_TITLE]] =\
                     Tree_Ancestor_Indexer.index[SUBKEY_PAGE][page[SUBKEY_TITLE]].\
                     union(self.node_supercategories).\
                     union(set([self.node_value[CM_TITLE]]))
        except AttributeError as ae:
            pass
        try:
            for sub_node in self.node_data.sub_nodes:
                Tree_Ancestor_Indexer.index[SUBKEY_SUBCAT][sub_node._node_params[CM_TITLE]] = \
                         Tree_Ancestor_Indexer.index[SUBKEY_SUBCAT][sub_node._node_params[CM_TITLE]].\
                         union(self.node_supercategories).union(set([self.node_value[CM_TITLE]]))
                subcat_indexer = Node_Indexer(sub_node, 
                                              Tree_Ancestor_Indexer.index[SUBKEY_SUBCAT][sub_node._node_params[CM_TITLE]])
                subcat_indexer.index()
        except AttributeError as ae:
            pass
            
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
    
    def initiate_from_file(self, file_name):
        '''
        Input file must be a data file saved using tree data class
        '''
        self.tree = Tree_Data.load_from_file(file_name)
        
    def run_index(self, filter_function = lambda x: x ):
        root_indexer = Node_Indexer(self.tree.root, [])
#         root_indexer = Node_Indexer(self.tree.root, set())
        root_indexer.index()
        counter = 0
        for key in Tree_Ancestor_Indexer.index[SUBKEY_PAGE]:
            if counter < 100:
                print key + ' ' + str(Tree_Ancestor_Indexer.index[SUBKEY_PAGE][key])
                counter += 1
        self.number_of_pages = len(Tree_Ancestor_Indexer.index[SUBKEY_PAGE])
        print self.number_of_pages
        self.number_of_subcats = len(Tree_Ancestor_Indexer.index[SUBKEY_SUBCAT])
        print self.number_of_subcats
        
    def query(self):
        pass
    
    def save_to_file(self, file_name):
        with open(file_name, 'w') as write_file:
            pickle.dump(Tree_Ancestor_Indexer.index, write_file)
    
    @classmethod
    def load_from_file(cls, file_name):
        with open(file_name, 'r') as read_file:
            Tree_Ancestor_Indexer.index = pickle.load(read_file)
