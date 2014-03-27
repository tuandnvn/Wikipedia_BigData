'''
Created on Mar 14, 2014

@author: Tuan
'''
import copy
import pickle

from brandeis.bigdata.wiki.crawler.category_crawler import Category_Crawler
from brandeis.bigdata.wiki.language_utils.named_entity import Named_Entity
from brandeis.bigdata.wiki.utils.constant import *


MAX = 1000
class Node_Data(object):
    '''
    Class to:
        - Recursively trace from a Wiki category page, to its sub-categories, and pages, and
        add into a hierarchical structures of Node_Data.
    '''
    def __init__(self, parent_node, node_param):
        '''
        node_params should be a dictionary and should provides the following keys:
                - cmtitle: The category of the node category page
            XOR 
                - cmpageid: Page ID of the node category page
        '''
        self.parent_node = parent_node
        self._node_params = node_param
        self.sub_nodes = []
        if parent_node != None:
            self.level = parent_node.level + 1
        else:
            self.level = 0 
        
#         if self.level == 1:
#             print 
        
    def crawl_data(self):
        if Tree_Data.counter > MAX:
            return
        """
        Crawl all pages
        """
        temp_params = copy.deepcopy(self._node_params)
        temp_params[CM_SORT] = SUBKEY_SORTKEY
        temp_params[CM_START_SORT_KEY] = 'A'
        temp_params[CM_END_SORT_KEY] = 'Z'
        temp_params[CM_DIRECTION_SORT] = SUBKEY_ASC
        temp_params[CM_TYPE] = SUBKEY_PAGE
        
        self._crawler = Category_Crawler(temp_params)
        self._crawler.crawl()
        crawled = self._crawler.xml_parse()
        if crawled != None:
            self.pages = [{DATA_PAGEID: page[DATA_PAGEID],
                            DATA_TITLE: page[DATA_TITLE]} 
                           for page in crawled[SUBKEY_PAGE] if 
                           Named_Entity.is_name_candidate(page[SUBKEY_TITLE])]
            print len(self.pages)
        
        """
        Crawl all subcategories
        Category format:
        {'pageid': '14557890', 'ns': '14', 'type': 'subcats', 'title': 'Category:Economists by area of research'}
        """
        del temp_params[CM_START_SORT_KEY]
        del temp_params[CM_END_SORT_KEY]
        temp_params[CM_TYPE] = SUBKEY_SUBCAT
        
        self._crawler = Category_Crawler(temp_params)
        self._crawler.crawl()
        crawled = self._crawler.xml_parse()
        if crawled != None:
            self.subcats = [{DATA_PAGEID: subcat[DATA_PAGEID],
                            DATA_TITLE: subcat[DATA_TITLE]} 
                           for subcat in crawled[SUBKEY_SUBCAT]]
        
        """
        Crawl a special type of category:
        _____ by nationality
        """
        temp_params[CM_END_SORT_KEY] = 'A'
        
        special_str = NATIONALY_STR
        self._crawler = Category_Crawler(temp_params)
        self._crawler.crawl()
        crawled = self._crawler.xml_parse()
        if crawled != None:
            self.special_subcats = [{DATA_PAGEID: subcat[DATA_PAGEID],
                                     DATA_TITLE: subcat[DATA_TITLE]}  
                                   for subcat in crawled[SUBKEY_SUBCAT] if special_str in subcat[DATA_TITLE]]
        
        if 'subcats' in self.__dict__:
            for subcat in (self.subcats + self.special_subcats):
                if subcat[DATA_TITLE] not in Tree_Data.checked_subcat:
                    """
                    It is important to put this check first, 
                    because if it's put after subnode.crawl_data(),
                    a failing crawled node could run again and again. 
                    """
                    Tree_Data.checked_subcat[subcat[DATA_TITLE]] = 1
                    try:
                        print subcat[DATA_TITLE]
                        Tree_Data.counter += 1
                        print Tree_Data.counter
                        if Tree_Data.counter > MAX:
                            Tree_Data.get_instance_without_initiate().save_to_file('Scientists_data_file.dat')
                    except UnicodeEncodeError as error:
                        print 'Couldn\'t print'
                        continue
                    subcat_params = {CM_TITLE: subcat[DATA_TITLE] }
                    subnode = Node_Data(self, subcat_params)
                    subnode.crawl_data()
                    
                    
                    self.sub_nodes.append(subnode)
    
class Tree_Data(object):
    '''
    Class to store a tree structure. Actually it is just the root Node, with some 
    more method to store and load to and from file.
    '''

    def __init__(self, root_params):
        '''
        root_params should be a dictionary and should provides the following keys:
                - cmtitle: The category of the root category page
            XOR 
                - cmpageid: Page ID of the root category page
        '''
        self._root_params = root_params
        self.root = Node_Data(None, root_params)
        
        Tree_Data.counter = 0
        """
        A class object to keep track of explored categories 
        """
        if CM_TITLE in self._root_params:
            Tree_Data.checked_subcat = {self._root_params[CM_TITLE]: 1}
    
    def crawl_data(self):
        self.root.crawl_data()
    
    def save_to_file(self, file_name):
        with open(file_name, 'w') as write_file:
            pickle.dump({ROOT_PARAM: self._root_params,
                         TREE: self.root}
                        , write_file)
    
    @classmethod
    def get_instance(cls, root_params):
        try:
            return cls.instance
        except AttributeError:
            cls.instance = Tree_Data(root_params)
            return cls.instance
    
    @classmethod
    def get_instance_without_initiate(cls):
        try:
            return cls.instance
        except AttributeError:
            return
        
    @classmethod
    def load_from_file(cls, file_name):
        with open(file_name, 'r') as read_file:
            o = pickle.load(read_file)
            _root_params = o[ROOT_PARAM]
            new_tree = Tree_Data(_root_params)
            new_tree.root = o[TREE]
            return new_tree
        
