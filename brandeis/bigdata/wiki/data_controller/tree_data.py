'''
Created on Mar 14, 2014

@author: Tuan
'''
import copy
import pickle

from brandeis.bigdata.wiki.crawler.category_crawler import Category_Crawler


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
            self.pages =  crawled['page']
            print len(self.pages)
        
        """
        Crawl all subcategories
        Category format:
        {'pageid': '14557890', 'ns': '14', 'type': 'subcat', 'title': 'Category:Economists by area of research'}
        """
        del temp_params['cmstartsortkey']
        del temp_params['cmendsortkey']
        temp_params['cmtype'] = 'subcat'
        
        self._crawler = Category_Crawler(temp_params)
        self._crawler.crawl()
        crawled = self._crawler.xml_parse()
        if crawled != None:
            self.subcat = crawled['subcat']
        
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
            self.special_subcat = [subcat for subcat in crawled['subcat'] if special_str in subcat['title']]
            self.subcat += self.special_subcat
        
        if 'subcat' in self.__dict__:
            for subcat in self.subcat:
                print subcat
                subcat_params = {'cmtitle': subcat['title'] }
                subnode = Node_Data( self, subcat_params )
                subnode.crawl_data()
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
        with open(file_name, 'w') as file:
            pickle.dump({'root_param': self._root_params,
                         'tree': self.root}
                        ,file)
    
    def load_from_file(self, file_name):
        with open(file_name, 'r') as file:
            o = pickle.load(file)
            self._root_params = o['root_param']
            self.root = o['tree']
        