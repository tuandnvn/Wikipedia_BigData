'''
Created on Mar 14, 2014

@author: Tuan
'''
import pickle
from collections import defaultdict
from brandeis.bigdata.wiki.data_controller.tree_data import Tree_Data


class Node_Indexer(object):
    def __init__(self, node_data, node_supercategories ):
        '''
        Wrap a Node_Data type object node_data
        Decorate it with indexing method
        '''
        self.node_data = node_data
        self.node_supercategories = node_supercategories
        
        self.node_value = {}
        if 'cmtitle' in self.node_data._node_params:
            self.node_value['cmtitle'] = self.node_data._node_params['cmtitle']
        if 'cmpageid' in self.node_data._node_params:
            self.node_value['cmpageid'] = self.node_data._node_params['cmpageid']
        
    def index(self):
        for page in self.node_data.pages:
            Tree_Indexer.index['page'][page['id']] = Tree_Indexer.index['page'][page['id']].union(self.node_supercategories).union(self.node_value)
        for subcat in self.node_data.subcats:
            Tree_Indexer.index['subcat'][subcat['id']] = Tree_Indexer.index['subcat'][subcat['id']].union(self.node_supercategories).union(self.node_value)
            
class Tree_Indexer(object):
    '''
    Index the hierarchical structure into an indexing of the following format:
    Dict[(person_name, person_id)] = [list of profession categories]
    '''
    def __init__(self):
        '''
        Tree_Indexer.index keep the index of the whole hierarchy
        '''
        Tree_Indexer.index = {'subcat': defaultdict(set),
                              'page': defaultdict(set)}
    
    def initiate_from_file(self, file_name):
        '''
        Input file must be a data file saved using tree data class
        '''
        self.tree = Tree_Data.load_from_file(file_name)
        
    def index(self):
        root_indexer = Node_Indexer(self.tree.root, {} )
        root_indexer.index()
        self.number_of_pages =  len(Tree_Indexer.index['page'])
        print self.number_of_pages
        self.number_of_subcats =  len(Tree_Indexer.index['subcat'])
        print self.number_of_subcats
        
    def query(self):
        pass
    
    def save_to_file(self, file_name):
        with open(file_name, 'w') as write_file:
            pickle.dump(Tree_Indexer.index, write_file)
    
    @classmethod
    def load_from_file(cls, file_name):
        with open(file_name, 'r') as read_file:
            Tree_Indexer.index = pickle.load(read_file)