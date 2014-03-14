'''
Created on Mar 14, 2014

@author: Tuan
'''

class Named_Entity(object):
    '''
    Util class to process named entity
    Every method related to named entity processing are put here
    '''


    def __init__(self, string_form):
        '''
        Taking the string form of the named entity as only input
        '''
        self.string_form = string_form
        
    def is_name_candidate(self):
        '''
        Name of people in Wikipedia is generally have the following format
        capitalized_name ( disambiguation_tag )
        For example:
        Ghulam Mohey-ud-din (economist)
        This function will heurictically tokenized and count the number of capitalized tokens in the named entity
        
        Issues:
        -    Couldn't distinguish between names of people and names of organizations.
        '''
        tokens = [token for token in self.string_form.split(' ') if (token[0] != '(' and token[-1] != ')')]
        capitalized = [token for token in tokens if token[0].isupper()]
        if 3*len(capitalized) >  2*len(tokens):
            return True
        return False
