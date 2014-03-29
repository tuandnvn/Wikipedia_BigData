'''
Created on Mar 14, 2014

@author: Tuan
'''
import unittest

from brandeis.bigdata.wiki.crawler.category_crawler import Category_Crawler
from brandeis.bigdata.wiki.data_controller.data_indexer import \
    Tree_Ancestor_Indexer
from brandeis.bigdata.wiki.data_controller.tree_data import Tree_Data
from brandeis.bigdata.wiki.language_utils.named_entity import Named_Entity


# class TestCrawl(unittest.TestCase):
# 
#     def setUp(self):
#         """
#         Test set up:
#         http://en.wikipedia.org/w/api.php?action=query&
#         list=categorymembers&cmtitle=Category:Economists&cmtype=page&cmstartsortkey=A&cmendsortkey=Z&
#         cmdir=asc&cmlimit=500&cmprop=ids|title|type&format=xml
#         """
#         page_params = {'cmtitle': 'Category:Economists', 
#                   'cmsort' : 'sortkey',
#                   'cmstartsortkey': 'A',
#                   'cmendsortkey': 'Z', 
#                   'cmdir' : 'asc',
#                   'cmtype': 'page'}
#         self.page_crawler = Category_Crawler(page_params)
#         
#         subcat_params = {'cmtitle': 'Category:Economists', 
#                   'cmtype': 'subcat'}
#         
#         self.subcat_crawler = Category_Crawler(subcat_params)
#     
#     def test_parse(self):
#         
#         self.assertTrue(self.page_crawler.crawl())
#         self.assertEqual(len(self.page_crawler.xml_parse()['page']), 52)
#         
#         self.assertTrue(self.subcat_crawler.crawl())
#         self.assertEqual(len(self.subcat_crawler.xml_parse()['subcat']), 11)
# class TestTreeData(unittest.TestCase):
#     def setUp(self):
#         """
#         Test Tree set up:
#             Root node: Economists
#         """
#         self.root_params = {'cmtitle': 'Category:Economists'}
#         self.test_file_name = 'Economist_test_file.dat'
#        
#     def testTree(self):
#         self.tree = Tree_Data(self.root_params)
#         self.tree.crawl_data()
#         self.tree.save_to_file(self.test_file_name)
#         self.assertEqual(len(self.tree.root.pages), 50)
#     def testLoadTree(self):
#         self.tree = Tree_Data(self.root_params)
#         self.tree.load_from_file(self.test_file_name)
# class TestTreeData2(unittest.TestCase):
#     def setUp(self):
#         """
#         Test Tree set up:
#             Root node: People_by_occupation
#         """
#         self.root_params = {'cmtitle': 'Category:People by occupation'}
#         self.test_file_name = 'Occupation_data_file.dat'
#       
#     def testTree(self):
#         self.tree = Tree_Data(self.root_params)
#         self.tree.crawl_data()
#         self.tree.save_to_file(self.test_file_name)

class TestTreeData3(unittest.TestCase):
    def setUp(self):
        """
        Test Tree set up:
            Root node: People_by_occupation
        """
        self.root_params = {'cmtitle': 'Category:Scientists'}
        self.test_file_name_prefix = 'Scientists_data_file_'
        self.test_file_name_ext = '.dat'
        self.number_of_expand_subcat = 70
             
    def testTree(self):
             
        self.tree = Tree_Data.get_instance(self.root_params)
        self.tree.crawl_data(self.number_of_expand_subcat)
        self.tree.save_to_file('%s%d%s' % (self.test_file_name_prefix,
                                           self.number_of_expand_subcat,
                                           self.test_file_name_ext))
        
# class TestResume(unittest.TestCase):
#     def setUp(self):
#         """
#         Test Tree set up:
#             Root node: Scientists
#         """
#         self.root_params = {'cmtitle': 'Category:Scientists'}
#         self.test_file_name_prefix = 'Scientists_data_file_'
#         self.test_file_name_ext = '.dat'
#         self.number_of_expand_subcat = 10
#         self.number_of_resume_expand_subcat = 20
#          
#     def testResuming(self):
#             
#         self.tree = Tree_Data.get_instance(self.root_params)
#         self.tree.crawl_data(self.number_of_expand_subcat)
#         data_file_1 = '%s%d%s' % (self.test_file_name_prefix,
#                                   self.number_of_expand_subcat,
#                                   self.test_file_name_ext)
#         self.tree.save_to_file(data_file_1)
#         data_file_2 = '%s%d%s' % (self.test_file_name_prefix,
#                                   self.number_of_resume_expand_subcat,
#                                   self.test_file_name_ext)
#         Tree_Data.resume_crawl_data(self.number_of_resume_expand_subcat,
#                                     data_file_1,
#                                     data_file_2)
#         self.tree = Tree_Data.get_instance_without_initiate()
#         self.tree.save_to_file(data_file_2)
        
# class TestIndexing(unittest.TestCase):
#     def setUp(self):
#         """
#         Setup data file
#         """
#         self.number_of_expand_subcat = 10000
#         self.input_file_name = 'Scientists_data_file_%d.dat' % self.number_of_expand_subcat
#         self.output_index_file_name = 'Scientists_raw_index_%d.dat' % self.number_of_expand_subcat
#         
#         self.readable_index_file_name = 'Scientists_after_filter_%d.txt' % self.number_of_expand_subcat
#         self.histogram_file_name = 'Scientists_histogram_%d.txt' % self.number_of_expand_subcat
#         self.processed_flat_index = 'Scientists_after_filter_index_%d.txt' % self.number_of_expand_subcat
#            
#     def testIndexing(self):
#         tree_indexer = Tree_Ancestor_Indexer()
#         tree_indexer.initiate_from_file(self.input_file_name)
#         tree_indexer.run_index()
#         tree_indexer.post_process_indexing_filter_profession()
#         tree_indexer.save_profession_histogram(self.histogram_file_name)
#         tree_indexer.save_flat_index(self.processed_flat_index)
#         tree_indexer.print_readable_to_file(self.readable_index_file_name)

# class TestFilterStatistically(unittest.TestCase):
#     def setUp(self):
#         """
#         Setup data file
#         """
#         self.number_of_expand_subcat = 10000
#         self.input_histogram_file_name = 'Scientists_histogram_%d.txt' % self.number_of_expand_subcat
#         self.input_processed_flat_index = 'Scientists_after_filter_index_%d.txt' % self.number_of_expand_subcat
#         self.LOW_THRESHOLD = 20
#         
#         self.output_histogram_file_name = 'Scientists_histogram_statistics_%d.txt' % self.number_of_expand_subcat
#         self.output_processed_flat_index = 'Scientists_after_statistics_%d.txt' % self.number_of_expand_subcat
#         self.readable_index_file_name = 'Scientists_readable_statistic_%d.txt' % self.number_of_expand_subcat
#         
#     
#     def testFilter(self):
#         tree_indexer = Tree_Ancestor_Indexer()
#         tree_indexer.load_profession_histogram(self.input_histogram_file_name)
#         tree_indexer.load_flat_index(self.input_processed_flat_index)
#         tree_indexer.post_process_indexing_statistic(self.LOW_THRESHOLD)
#         
#         tree_indexer.save_profession_histogram(self.output_histogram_file_name)
#         tree_indexer.save_flat_index(self.output_processed_flat_index)
#         tree_indexer.print_readable_to_file(self.readable_index_file_name)

        
# class TestProfessionStringTransform(unittest.TestCase):
#     def setUp(self):
#         Named_Entity.loadNationality()
#      
#     def testTransforming(self):
#         test_cases = [('Category:South African linguists', 'linguist'),
#                       ('Category:American astronomers', 'astronomer'),
#                       ('Category:Romanian botanists', 'botanist'),
#                       ('Category:American zoologist stubs', 'zoologist'),
#                       ('Category:Marine biologists by nationality', 'marine biologist')
#                       ]
#         for test_case in test_cases:
#             self.assertEqual(test_case[1], Profession_Name_Entity.professionCategoryTransform(test_case[0]))
        
if __name__ == '__main__':
    unittest.main()
