'''
Created on Mar 14, 2014

@author: Tuan
'''
"""
Some other thing to do:
remove Category:Something by someone
remove Category:Person_proper_name 
"""

from bisect import bisect_left
import codecs
import json
import os

from brandeis.bigdata.wiki import ROOT_DIRECTORY
from brandeis.bigdata.wiki.utils.constant import *

class IncorrectIndexException(Exception):
    """
    Auxillary exception class to bubble up the exception 
    when it found a string form in the profession of an index that 
    doesn't look relevant.
    For example:
    Alpha Corvi [u'natural philosopher', u'scientist', u'constellations listed', u'ptolemy']
    When string form 'constellations' is found, it's suspected that
    the page is mistakenly indexed.
    Therefore exception is bubbled up to higher level of processing. 
    General handling with this exception is dropping the whole index 
    """
    def __init__(self, string_form):
        Exception.__init__(self, string_form)


class Named_Entity():
    '''
    Util class to process named entity
    Every method related to named entity processing are put here
    '''
    LANG_DIRECTORY_DATA = os.path.join(ROOT_DIRECTORY, 'language_utils', 'data')
    
    class People_Name_Entity():
        '''
        Class for all methods related to name string form of a person
        '''
        @classmethod
        def isNameCandidate(cls, string_form):
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
            if 3 * len(capitalized) > 2 * len(tokens):
                return True
            return False
    
    class Profession_Name_Entity():
        NATIONALITY_RAW_FILE_NAME = 'nationalities.txt'
        NATIONALITY_STRUCT_FILE_NAME = 'nationalities_struct_list.dict'
        NATIONALITY_FLAT_FILE_NAME = 'nationalities_flat_list.dict'
        
        @classmethod
        def processNationalities(cls):
            """
            Process the nationalities file to get adjective forms and demonym form 
            The file has the following generative grammar:
            Nationality_line -> Place_names : Place_adj_demonym       (1)
            Place_adj_demonym -> Noun_forms ; Adjective_forms         (2)
            Place_names -> Place_name( ; Place_name)*                (3)
            Noun_forms -> EMPTY | noun--Alternative_noun_forms        (4)
            Adj_forms -> EMPTY | adjective--Alternative_adj_forms     (5)
            Alternative_noun_forms -> noun_form ( or noun_form )*     (6)
            Alternative_adj_forms -> adj_form ( or adj_form )*        (7)
            noun_form -> noun_str(\(s\))*
            """
            nationalities_flat_form = []
            nationalities_structured_form = []
            NATIONALITY_FILE = os.path.join(cls.LANG_DIRECTORY_DATA, cls.NATIONALITY_RAW_FILE_NAME)
            
            def split_1(str_form):
                """
                Split according to generative grammar rule 1
                """
                str_form = str_form.strip()
                return str_form.split(':')
            
            def split_2(str_form):
                """
                Split according to generative grammar rule 2
                """
                return str_form.strip().split(DIFF_CAT_SEPARATE)
            
            def split_3(str_form):
                """
                Split according to generative grammar rule 3
                """
                names = str_form.split(NATIONAL_NAME_SEPARATE)
                return [name.strip() for name in names]
            
            def split_4_6(str_form):
                """
                Split according to generative grammar rule 4 and 6
                """
                noun_forms = []
                if str_form.strip()[:len(NOUN_PREFIX)] == NOUN_PREFIX:
                        nouns = str_form.strip()[len(NOUN_PREFIX):].split(SAME_CAT_SEPARATE)
                        for noun in nouns:
                            if noun[-3:] == PLURAL_STR:
                                single_form = noun[:-3].strip()
                                plural_form = single_form + PLURAL_SUFFIX
                                noun_forms.append(single_form)
                                noun_forms.append(plural_form)
                            else:
                                noun_forms.append(noun.strip())
                return noun_forms
            
            def split_5_7(str_form):
                """
                Split according to generative grammar rule 5 and 7
                """
                adj_forms = []
                if str_form.strip()[:len(ADJ_PREFIX)] == ADJ_PREFIX:
                    adjs = str_form.strip()[len(ADJ_PREFIX):].split(SAME_CAT_SEPARATE)
                    adj_forms = [adj.strip() for adj in adjs]
                return adj_forms
            
            def split_file_line(line):
                nationality = {}
                nation_names, nationality_forms = split_1(line)
                nationality[NATIONAL_NAME] = split_3(nation_names)
                
                noun_form, adjective_form = split_2(nationality_forms)
                nationality[NATIONALITY_NFORM] = split_4_6(noun_form)
                nationality[NATIONALITY_AFORM] = split_5_7(adjective_form)
                return nationality
            
            def update_nationality_str_form_data(nationality):
                """
                Update the structured form
                """
                nationalities_structured_form += nationality[NATIONAL_NAME]
                nationalities_structured_form += nationality[NATIONALITY_NFORM]
                nationalities_structured_form += nationality[NATIONALITY_AFORM]
                
                """
                Update the flat form
                """
                nationalities_flat_form.append(nationality)
            
            def save_nationality_str_form_data_to_file(structured_file, flat_file):
                with open(flat_file, 'w') as file_handler:
                    json.dump(nationalities_flat_form, file_handler)
                with open(structured_file) as file_handler:
                    json.dump(nationalities_structured_form, file_handler)
                
            with codecs.open(NATIONALITY_FILE) as file_handler:
                for line in file_handler:
                    nationality = split_file_line(line)
                    update_nationality_str_form_data(nationality)
                    
            """
            Account for some lacking from the nationalities.txt file
            This constants set is not exhaustive,
            expect update from Amin for additional nationalities
            """
            nationalities_structured_form += ADDTIONAL_NATIONALITIES
            nationalities_structured_form = list(set(nationalities_structured_form))
            nationalities_structured_form.sort()
            
            structured_file = os.path.join(cls.LANG_DIRECTORY_DATA, cls.NATIONALITY_STRUCT_FILE_NAME)
            flat_file = os.path.join(cls.LANG_DIRECTORY_DATA, cls.NATIONALITY_FLAT_FILE_NAME)
            save_nationality_str_form_data_to_file (structured_file, flat_file)
        
        @classmethod
        def loadNationality(cls):
            with open(os.path.join(cls.LANG_DIRECTORY_DATA,
                                   'nationalities_flat_list.dict'), 'r') as file_handler:
                cls.nationalities_str_form = json.load(file_handler)
        
        @classmethod
        def getFirstToken(cls, profession_str_form):
            """
            Get first token of a string form only
            """
            index = profession_str_form.find(' ')
            return profession_str_form[:index]
        
        @classmethod
        def getSingularLowerForm(cls, profession_str_form):
            """
            A simple function get singular form 
            """
            profession_str_form = profession_str_form.lower()
            if profession_str_form[-1:] == 's':
                profession_str_form = profession_str_form[:-1]
            return profession_str_form
            
        @classmethod
        def deleteNationality(cls, profession_str_form):
            """
            Remove nationality Adj form at the begining of a profession candidate
            Only bisecting the professional list based on 
            the first token of string form.
            For example: if the str_form is 
            South Korean biologist
            we will compare South and Southzzzzzzzzzz 
            with the list of nationalities using bisect 
            and expect the index of South Korean to be
            between indices of South and  Southzzzzzzzzzz
            """
            first_token = cls.getFirstToken(profession_str_form)
            index_left = bisect_left(cls.nationalities_str_form, first_token)
            LAST_SUFFIX = 'zzzzzzzzzzzzzzzzz'
            index_right = bisect_left(cls.nationalities_str_form, first_token + LAST_SUFFIX)
            for index in xrange(index_left, index_right):
                national_form = cls.nationalities_str_form[index]
                if profession_str_form[:len(national_form) + 1] == national_form + ' ':
                    profession_str_form = profession_str_form[len(national_form):].strip()
            return profession_str_form.strip()
        
        @classmethod
        def deleteTimeExp(cls, profession_str_form):
            '''
            Delete something like 19th-century at the beginning of professions
            some other forms could -era, dynasty
            '''
            first_token = cls.getFirstToken(profession_str_form)
            for string in TEMPORAL_PREFIX:
                if first_token[-len(string):] == string:
                    profession_str_form = profession_str_form[len(first_token)].strip()
            return profession_str_form
            
        @classmethod
        def deleteIrrelevantLastWord(cls, profession_str_form):
            '''
            Delete sth like 'stubs' at the end 
            '''
            for string in OTHER_DELETE_SUFFIX:
                if profession_str_form[-len(string):] == string:
                    return profession_str_form[:-len(string)].strip()
            return profession_str_form
        
        @classmethod
        def deleteCategory(cls, profession_str_form):
            '''
            Delete Category: string at the begining
            '''
            if profession_str_form[:len(CATEGORY_PRE)] == CATEGORY_PRE:
                profession_str_form = profession_str_form[len(CATEGORY_PRE):]
            return profession_str_form
        
        @classmethod
        def deletePreposition(cls, profession_str_form):
            '''
            Remove all prepositions:
            translators from UK
            translators to English
            translators who receive ...
            '''
            for prepositional_str in PREPOSITION_STR:
                prepositional_index = profession_str_form.find(prepositional_str)
                if prepositional_index != -1:
                    profession_str_form = profession_str_form[:prepositional_index]
            return profession_str_form
        
        @classmethod
        def deleteGender(cls, profession_str_form):
            '''
            Delete gender string form
            '''
            for gender_str in GENDER_STR_FORM:
                gender_index = profession_str_form.find(gender_str)
                if gender_index != -1:
                    profession_str_form = profession_str_form[gender_index + len(gender_str):].strip()
            return profession_str_form
        
        @classmethod
        def deleteSpecialStatePrefix(cls, profession_str_form):
            """
            Need to be executed before deleteNationality
            Delete some prefix of nationality such as: 
            Imperial, Medieval, Ancient
            """
            for special_state_prefix in SPECIAL_STATE_STR_FORM:
                if profession_str_form[:len(special_state_prefix)] == special_state_prefix:
                    profession_str_form = profession_str_form[len(special_state_prefix):]
            return profession_str_form
            
        @classmethod
        def filterMistakenCategory(cls, profession_str_form):
            '''
            Some profession string form is mistakenly
            crawled
            '''
            for mistaken_form in MISTAKEN_CATEGORY_STR_FORMS:
                if profession_str_form.find(mistaken_form) != -1:
                    return None
            
            return profession_str_form
        
        @classmethod
        def feedbackMistakenIndex(cls, profession_str_form):
            '''
            Some profession string form could signal
            that the index is incorrectly crawled
            by unpredictable reasons. For example, names of
            constellations and names of glaciers could be 
            crawled out of expectation. 
            '''
            for mistaken_form in MISTAKEN_INDEX_STR_FORMS:
                if profession_str_form == mistaken_form:
                    raise IncorrectIndexException("Mistaken form is " + profession_str_form)
        @classmethod
        def professionCategoryTransform(cls, category_str) :
            modify_stream_works = [cls.deleteCategory, cls.deletePreposition, 
                                   cls.deleteIrrelevantLastWord, cls.deleteSpecialStatePrefix,
                                   cls.deleteNationality, cls.deleteTimeExp,
                                   cls.deleteGender,
                                   cls.getSingularLowerForm] #getSingularLowerForm should always be the last
            delete_stream_works = [cls.filterMistakenCategory] # should always at the end
                                                                # cause it might return NULL
            exception_stream_works = [cls.feedbackMistakenIndex]
            
            for stream_work in modify_stream_works:
                category_str = stream_work(category_str)
            for stream_work in delete_stream_works:
                category_str = stream_work(category_str)
            for stream_work in exception_stream_works:
                try:
                    stream_work(category_str)
                except IncorrectIndexException as e:
                    raise e
                return category_str

# Named_Entity.processNationalities()
