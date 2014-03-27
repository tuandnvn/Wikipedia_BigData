'''
Created on Mar 14, 2014

@author: Tuan
'''
"""
Some other thing to do:
remove Category:Something by someone
remove Category:Person_proper_name 
"""
class Named_Entity():
    '''
    Util class to process named entity
    Every method related to named entity processing are put here
    '''


    def __init__(self):
        '''
        Taking the string form of the named entity as only input
        '''
        pass
    
    @classmethod
    def is_name_candidate( cls, string_form ):
        '''
        Name of people in Wikipedia is generally have the following format
        capitalized_name ( disambiguation_tag )
        For example:
        Ghulam Mohey-ud-din (economist)
        This function will heurictically tokenized and count the number of capitalized tokens in the named entity
        
        Issues:
        -    Couldn't distinguish between names of people and names of organizations.
        '''
        tokens = [token for token in string_form.split(' ') if (token[0] != '(' and token[-1] != ')')]
        capitalized = [token for token in tokens if token[0].isupper()]
        if 3*len(capitalized) >  2*len(tokens):
            return True
        return False
