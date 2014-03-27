'''
Created on Mar 14, 2014

@author: Tuan
'''

import copy
import re
import urllib

import lxml

from brandeis.bigdata.wiki.utils.constant import *
import xml.etree.ElementTree as ET


class Category_Crawler(object):
    '''
    """
    This category link is crawled based on category API of wikipedia.
    http://www.mediawiki.org/wiki/API:Categorymembers.
    Begin from the highest node in 
    """
    '''


    def __init__(self, params):
        '''
         The full set of keys as provided from the API are supported. 
         Params should be a dictionary and should provides the following keys:
                - cmtitle: The category to enumerate. Must include Category: prefix
            XOR 
                - cmpageid: Page ID of the category to enumerate. Cannot be used together with cmtitle.
        '''
        
        self._configurations = copy.deepcopy(params)
        """
        Checking the conditions of params to avoid unacceptable key in the params
        """
        for key in self._configurations:
            if key not in KEY_SET:
                del self._configurations[key]
        
        if CM_TITLE in self._configurations and CM_PAGEID in self._configurations:
            """
            Just use 'cmpageid'
            """
            del self._configurations[CM_TITLE]
        
        for key in CONSTRAINTS:
            if key in self._configurations:
                values = self._configurations[key].split(CONJUNCTION)
                values = [value for value in values if value in CONSTRAINTS[key]]
                self._configurations[key] = CONJUNCTION.join(values)
                        
        # Additional configurations
        for key in DEFAULT_PARAMETERS:
            if not key in self._configurations:
                self._configurations[key] = DEFAULT_PARAMETERS[key]
        
        self._link = '%s%s&%s' % (WIKIPEDIA_API, QUERY_ACTION, CATEGORY_SUBACTION)
        for key in self._configurations:
            self._link += '&%s=%s' % (key, self._configurations[key])
    
    def get_link(self):
        return self._link
    
    def crawl(self):
        self.buffer = None
        try:
            streaming = urllib.urlopen(self._link)
            self.buffer = "";
            for line in streaming:
                self.buffer += line
            return True
        except IOError as io_error:
            print 'Connection could not be established.\nFail to crawl the wiki xml file.'
            return False
        except UnicodeError as io_error:
            print 'Unicode character. Ignored.'
            return False
            
    
    def xml_parse(self):
        """
        Format of the xml file returned
        <api>
            <query>
                <categorymembers>
                    <cm pageid="15020927" ns="0" title="Bon Yeon"/>
                </categorymembers>
            </query>
        </api>
        """
        if self.buffer == None:
            return None
        root = ET.fromstring(self.buffer)
        
        cms = root.find(QUERY_TAG).find(CATEGORY_TAG).findall(CATEGORY_CM_TAG)
        results = {SUBKEY_PAGE:[], SUBKEY_SUBCAT:[]}
        for cm in cms:
            if cm.attrib[SUBKEY_TYPE] == SUBKEY_PAGE or cm.attrib[SUBKEY_TYPE] == SUBKEY_SUBCAT:
                results[cm.attrib[SUBKEY_TYPE]].append((cm.attrib))
        return results