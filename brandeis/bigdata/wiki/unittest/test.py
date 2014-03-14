'''
Created on Mar 14, 2014

@author: Tuan
'''
import unittest

from brandeis.bigdata.wiki.crawler.category_crawler import Category_Crawler
from brandeis.bigdata.wiki.data_controller.tree_data import Tree_Data


class TestCrawl(unittest.TestCase):

    def setUp(self):
        """
        Test set up:
        http://en.wikipedia.org/w/api.php?action=query&
        list=categorymembers&cmtitle=Category:Economists&cmtype=page&cmstartsortkey=A&cmendsortkey=Z&
        cmdir=asc&cmlimit=500&cmprop=ids|title|type&format=xml
        """
        page_params = {'cmtitle': 'Category:Economists', 
                  'cmsort' : 'sortkey',
                  'cmstartsortkey': 'A',
                  'cmendsortkey': 'Z', 
                  'cmdir' : 'asc',
                  'cmtype': 'page'}
        self.page_crawler = Category_Crawler(page_params)
        
        subcat_params = {'cmtitle': 'Category:Economists', 
                  'cmtype': 'subcat'}
        
        self.subcat_crawler = Category_Crawler(subcat_params)
    
    def test_parse(self):
        
        self.assertTrue(self.page_crawler.crawl())
        self.assertEqual(len(self.page_crawler.xml_parse()['page']), 52)
        
        self.assertTrue(self.subcat_crawler.crawl())
        self.assertEqual(len(self.subcat_crawler.xml_parse()['subcat']), 11)

class TestTreeData(unittest.TestCase):
    def setUp(self):
        """
        Test Tree set up:
            Root node: Azerbaijani economists
        """
#         self.root_params = {'cmtitle': 'Category:Azerbaijani economists'}
        self.root_params = {'cmtitle': 'Category:Economists'}
        self.test_file_name = 'test_file.dat'
    
    def testTree(self):
        self.tree = Tree_Data(self.root_params)
        self.tree.crawl_data()
        self.tree.save_to_file(self.test_file_name)
#         self.assertEqual(len(self.tree.root.pages), 6)
    
    def testLoadTree(self):
        self.tree = Tree_Data(self.root_params)
        self.tree.load_from_file(self.test_file_name)
#         self.assertEqual(self.tree.root.pages[0], {'pageid': '12794963', 'ns': '0', 'type': 'page', 'title': 'Avaz Alakbarov'})
        
if __name__ == '__main__':
    unittest.main()