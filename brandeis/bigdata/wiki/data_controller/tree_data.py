'''
Created on Mar 14, 2014

@author: Tuan
'''

import copy
import pickle

from brandeis.bigdata.wiki.crawler.category_crawler import Category_Crawler
from brandeis.bigdata.wiki.language_utils.named_entity import Named_Entity
from brandeis.bigdata.wiki.utils.constant import *


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
    
    def crawl_data(self, number_of_expand_subcat):
        '''
        Crawl the hierarchical data and put into a tree structure 
        Arguments: - number_of_expand_subcat: is the maximum number of categories
                    should be checked the content: pages and sub-categories
        '''
        print "===============Crawl================"
        Tree_Data.number_of_expand_subcat = number_of_expand_subcat
        self.root.crawl_data()
    
#     @classmethod
#     def resume_crawl_data(cls, number_of_expand_subcat,
#                           input_resume_file_name,
#                           output_resume_file_name):
#         print "===============Resume crawl================"
#         cls.number_of_expand_subcat = number_of_expand_subcat
#         cls.resume_file_name = output_resume_file_name
#         cls.instance = cls.load_from_file(input_resume_file_name)
#         Tree_Data.checked_subcat = 0
#         cls.instance.root.resume_crawl_data()
    
    def save_to_file(self, file_name):
        '''
        Save the whole tree structure into a file, include
        the parameters in the root_param.
        Format of file: dictionary {ROOT_PARAM: dict _root_params,
                                     TREE: Node_Data root} 
        Arguments: file_name: file name to be saved in
        '''
        with open(file_name, 'w') as write_file:
            pickle.dump({ROOT_PARAM: self._root_params,
                         TREE: self.root 
#                          ,TREE_CHECKED: Tree_Data.checked_subcat
                         }
                        , write_file)
    
    @classmethod
    def get_instance(cls, root_params):
        '''
        Return the singleton of the class, given the parameters
        '''
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
        '''
        Classmethod to load the tree from a file (has been save beforehand by save_to_file)
        '''
        with open(file_name, 'r') as read_file:
            o = pickle.load(read_file)
            _root_params = o[ROOT_PARAM]
            new_tree = Tree_Data(_root_params)
            new_tree.root = o[TREE]
#             Tree_Data.checked_subcat = o[TREE_CHECKED]
            print Tree_Data.checked_subcat
            return new_tree
        
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
        
        """
        mark if the node is crawl yet, 
        used for resuming 
        """
        self.is_marked = False 
    
    @classmethod
    def check_limit_condition(cls):
        '''
        Check if the current node should be
        expand or not
        '''
        if Tree_Data.counter > Tree_Data.number_of_expand_subcat:
            return True
        return False
    
    def set_up_page_parameters(self):
        '''
        Set up parameters to crawl all pages having 
        initial letter from 'A' to 'Z' (we only
        crawl people names)
        '''
        parameters = copy.deepcopy(self._node_params)
        parameters[CM_SORT] = SUBKEY_SORTKEY
        parameters[CM_START_SORT_KEY] = 'A'
        parameters[CM_END_SORT_KEY] = 'Z'
        parameters[CM_DIRECTION_SORT] = SUBKEY_ASC
        parameters[CM_TYPE] = SUBKEY_PAGE
        return parameters
    
    def set_up_subcategory_parameters(self):
        '''
        Set up parameters to crawl all categories
        '''
        parameters = copy.deepcopy(self._node_params)
        parameters[CM_SORT] = SUBKEY_SORTKEY
        parameters[CM_DIRECTION_SORT] = SUBKEY_ASC
        parameters[CM_TYPE] = SUBKEY_SUBCAT
        return parameters
    
    def set_up_special_subcategory_parameters(self):
        '''
        Set up parameters to crawl some special categories
        one that have type:
        List of ....
        '''
        parameters = copy.deepcopy(self._node_params)
        parameters[CM_SORT] = SUBKEY_SORTKEY
        parameters[CM_DIRECTION_SORT] = SUBKEY_ASC
        parameters[CM_TYPE] = SUBKEY_SUBCAT
        parameters[CM_END_SORT_KEY] = 'A'
        return parameters
    
    def crawl_pages(self, parameters):
        '''
        Crawl pages given the parameters.
        Check if the page is name candidate (initial uppercase)
        '''
        self._crawler = Category_Crawler(parameters)
        self._crawler.crawl()
        crawled = self._crawler.xml_parse()
        if crawled != None:
            self.pages = [{DATA_PAGEID: page[DATA_PAGEID],
                            DATA_TITLE: page[DATA_TITLE]} 
                           for page in crawled[SUBKEY_PAGE] if 
                           Named_Entity.People_Name_Entity.isNameCandidate(page[SUBKEY_TITLE])]
    
    def crawl_subcategories(self, parameters):
        '''
        Crawl sub categories given the parameters.
        '''
        self._crawler = Category_Crawler(parameters)
        self._crawler.crawl()
        crawled = self._crawler.xml_parse()
        if crawled != None:
            self.subcats = [{DATA_PAGEID: subcat[DATA_PAGEID],
                            DATA_TITLE: subcat[DATA_TITLE]} 
                           for subcat in crawled[SUBKEY_SUBCAT]]
        else:
            self.subcats =[]
    
    def crawl_special_subcategories(self, parameters):
        '''
        Crawl special sub categories given the parameters.
        '''
        special_str = NATIONALY_STR
        self._crawler = Category_Crawler(parameters)
        self._crawler.crawl()
        crawled = self._crawler.xml_parse()
        if crawled != None:
            self.special_subcats = [{DATA_PAGEID: subcat[DATA_PAGEID],
                                     DATA_TITLE: subcat[DATA_TITLE]}  
                                   for subcat in crawled[SUBKEY_SUBCAT] if 
                                   special_str in subcat[DATA_TITLE]]
        else:
            self.special_subcats =[]
    
    def create_subnode(self, subcat):
        '''
        Create a subnode given the subcategory structure
        Arguments: subcat: dictionary has field DATA_TITLE
        '''
        """
        It is important to put this check first, 
        because if it's put after subnode.crawl_data(),
        a failing crawled node could run again and again. 
        """
        Tree_Data.checked_subcat[subcat[DATA_TITLE]] = 1
        Tree_Data.counter += 1
        if Tree_Data.counter % 10 == 0:
            print "Node.crawl ----- Tree_Data.counter " + str(Tree_Data.counter)
            print "Node.crawl ----- subcat[DATA_TITLE] " + subcat[DATA_TITLE]
        subcat_params = {CM_TITLE: subcat[DATA_TITLE] }
        subnode = Node_Data(self, subcat_params)
        return subnode
            
    def crawl_data(self):
        '''
        Crawl data based on different parameters and generate more tree structure
        '''
        if Node_Data.check_limit_condition():
            return
        
        """
        Crawl all pages
        """
        parameters = self.set_up_page_parameters()
        self.crawl_pages(parameters)
        
        """
        Crawl all subcategories
        Category format:
        {'pageid': '14557890', 'ns': '14', 'type': 'subcats', 'title': 'Category:Economists by area of research'}
        """
        parameters = self.set_up_subcategory_parameters()
        self.crawl_subcategories(parameters)
        
        """
        Crawl a special type of category:
        _____ by nationality
        """
        parameters = self.set_up_special_subcategory_parameters()
        self.crawl_special_subcategories(parameters)
    
        for subcat in (self.subcats + self.special_subcats):
            if subcat[DATA_TITLE] not in Tree_Data.checked_subcat:
                try:
                    subnode = self.create_subnode(subcat)
                except UnicodeEncodeError:
                    print 'Couldn\'t print'
                    continue
                subnode.crawl_data()
                self.sub_nodes.append(subnode)
                    
        self.is_marked = True
        
#     def resume_crawl_data(self):
#         if self.is_marked:
#             if 'sub_nodes' in self.__dict__:
#                 Tree_Data.counter += len(self.sub_nodes)
#                 for sub_node in self.sub_nodes:
#                     sub_node.resume_crawl_data()
#         else:
#             self.crawl_data()
            
