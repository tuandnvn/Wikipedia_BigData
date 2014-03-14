'''
Created on Mar 14, 2014

@author: Tuan
'''
from brandeis.bigdata.wiki.data_controller.tree_data import Tree_Data


class DataIndexer(object):
    '''
    Index the hierarchical structure into an indexing of the following format:
    Dict[(person_name, person_id)] = [list of profession categories]
    '''
    def __init__(self, file_name ):
        '''
        Input file must be a data file saved using tree data class
        '''
        self.tree = Tree_Data.load_from_file(file_name)
    
    def index(self):
        
        pass
    def query(self):
        pass