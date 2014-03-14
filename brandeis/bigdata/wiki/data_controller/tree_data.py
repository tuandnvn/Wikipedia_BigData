'''
Created on Mar 14, 2014

@author: Tuan
'''
import copy
import pickle

from brandeis.bigdata.wiki.crawler.category_crawler import Category_Crawler
from brandeis.bigdata.wiki.language_utils.named_entity import Named_Entity


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
        """
        A class object to keep track of explored categories 
        """
        if 'cmtitle' in node_param:
            Node_Data.checked_subcat = {node_param['cmtitle']: 1}
    
    def crawl_data(self):
        """
        Crawl all pages
        """
        temp_params = copy.deepcopy(self._node_params)
        temp_params['cmsort'] = 'sortkey'
        temp_params['cmstartsortkey'] = 'A'
        temp_params['cmendsortkey'] = 'Z'
        temp_params['cmdir'] = 'asc'
        temp_params['cmtype'] = 'page'
        
        self._crawler = Category_Crawler(temp_params)
        self._crawler.crawl()
        crawled = self._crawler.xml_parse()
        if crawled != None:
            self.pages =  [{'pageid': page['pageid'], 
                            'title': page['title']} 
                           for page in crawled['page'] if Named_Entity.is_name_candidate(page['title'])]
            print len(self.pages)
        
        """
        Crawl all subcategories
        Category format:
        {'pageid': '14557890', 'ns': '14', 'type': 'subcats', 'title': 'Category:Economists by area of research'}
        """
        del temp_params['cmstartsortkey']
        del temp_params['cmendsortkey']
        temp_params['cmtype'] = 'subcats'
        
        self._crawler = Category_Crawler(temp_params)
        self._crawler.crawl()
        crawled = self._crawler.xml_parse()
        if crawled != None:
            self.subcats = [{'pageid': subcat['pageid'], 
                            'title': subcat['title']} 
                           for subcat in crawled['subcats']]
        
        """
        Crawl a special type of category:
        _____ by nationality
        """
        temp_params['cmendsortkey'] = 'A'
        
        special_str = 'by nationality'
        self._crawler = Category_Crawler(temp_params)
        self._crawler.crawl()
        crawled = self._crawler.xml_parse()
        if crawled != None:
            self.special_subcat = [{'pageid': subcat['pageid'], 
                                    'title': subcat['title']} 
                                   for subcat in crawled['subcats'] if special_str in subcat['title']]
            self.subcats += self.special_subcat
        
        if 'subcats' in self.__dict__:
            for subcat in self.subcats:
                print subcat
                if subcat['title'] not in Node_Data.checked_subcat:
                    subcat_params = {'cmtitle': subcat['title'] }
                    subnode = Node_Data( self, subcat_params )
                    subnode.crawl_data()
                    Node_Data.checked_subcat[subcat['title']] = 1
                    self.sub_nodes.append( subnode )
    
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
    
    def crawl_data(self):
        self.root.crawl_data()
    
    def save_to_file(self, file_name):
        with open(file_name, 'w') as write_file:
            pickle.dump({'root_param': self._root_params,
                         'tree': self.root}
                        ,write_file)
    
    @classmethod
    def load_from_file( cls, file_name):
        with open(file_name, 'r') as read_file:
            o = pickle.load(read_file)
            _root_params = o['root_param']
            new_tree = Tree_Data(_root_params)
            new_tree.root = o['tree']
            return new_tree
        