'''
Created on Mar 27, 2014

@author: Tuan
'''

"""
Query constants
Semantics of the following constant keywords should be checked at
http://www.mediawiki.org/wiki/API:Categorymembers.
"""
CM_TITLE = 'cmtitle'  # category title
CM_PAGEID = 'cmpageid'  #
CM_NAMESPACE = 'cmnamespace'
CM_TYPE = 'cmtype'
CM_START = 'cmstart'
CM_END = 'cmend'
CM_START_SORT_KEY = 'cmstartsortkey'
CM_END_SORT_KEY = 'cmendsortkey'
CM_START_SORT_KEY_PRE = 'cmstartsortkeyprefix'
CM_END_SORT_KEY_PRE = 'cmendsortkeyprefix' 
CM_SORT = 'cmsort'  # Sort by what
CM_DIRECTION_SORT = 'cmdir'  # Small to large
CM_LIMIT_PAGE = 'cmlimit'  # Limit of pages returned by query
CM_PROPERTY = 'cmprop'  # Property of each page returned
CM_CONTINUE = 'cmcontinue'
FORMAT = 'format'

KEY_SET = [CM_TITLE, CM_PAGEID, CM_NAMESPACE, CM_TYPE,
           CM_START, CM_END, CM_START_SORT_KEY,
           CM_END_SORT_KEY, CM_START_SORT_KEY_PRE,
           CM_END_SORT_KEY_PRE, CM_SORT, CM_DIRECTION_SORT,
           CM_LIMIT_PAGE, CM_PROPERTY, CM_CONTINUE]

SUBKEY_PAGE = 'page'
SUBKEY_SUBCAT = 'subcat'
SUBKEY_FILE = 'file'

SUBKEY_SORTKEY = 'sortkey'
SUBKEY_TIMESTAMP = 'timestamp'

SUBKEY_ASC = 'asc'
SUBKEY_DESC = 'desc'

SUBKEY_IDS = 'ids'
SUBKEY_TITLE = 'title'
SUBKEY_SORTKEY = 'sortkey'
SUBKEY_SORTKEY_PRE = 'sortkeyprefix'
SUBKEY_TYPE = 'type'
SUBKEY_TIMESTAMP = 'timestamp'
CONJUNCTION = '|'


CONSTRAINTS = {CM_TYPE : [SUBKEY_PAGE, SUBKEY_SUBCAT, SUBKEY_FILE],
               CM_SORT: [SUBKEY_SORTKEY, SUBKEY_TIMESTAMP],
               CM_DIRECTION_SORT: [SUBKEY_ASC, SUBKEY_DESC],
               CM_PROPERTY: [SUBKEY_IDS, SUBKEY_TITLE, SUBKEY_SORTKEY,
                             SUBKEY_SORTKEY_PRE, SUBKEY_TYPE, SUBKEY_TIMESTAMP]}

DEFAULT_PARAMETERS = {CM_LIMIT_PAGE: '500',
                      CM_PROPERTY: '%s%s%s%s%s' % (SUBKEY_IDS , CONJUNCTION, SUBKEY_TITLE , 
                                                   CONJUNCTION, SUBKEY_TYPE),
                      FORMAT : 'xml'}

WIKIPEDIA_API = 'http://en.wikipedia.org/w/api.php?'
QUERY_ACTION = 'action=query'
CATEGORY_SUBACTION = 'list=categorymembers'

"""
Parsing xml data constants
"""
QUERY_TAG = 'query'
CATEGORY_TAG = 'categorymembers'
CATEGORY_CM_TAG = 'cm'


"""
Data constants
"""
DATA_PAGEID = 'pageid'
DATA_TITLE = 'title'
ROOT_PARAM = 'root_param'
TREE = 'tree'
TREE_COUNTER = 'tree_counter'
TREE_CHECKED = 'tree_checked'

"""
String process constants
"""
PREPOSITION_STR = [' by ', ' from ', ' at '
                   , ' in ', ' of ', ' who ', ' with ',
                   ' about ', ' to ']
NATIONALY_STR = 'by nationality'
CATEGORY_PRE = 'Category:'
NOUN_PREFIX = 'noun--'
ADJ_PREFIX = 'adjective--'
PLURAL_STR = '(s)'
PLURAL_SUFFIX = 's'
SAME_CAT_SEPARATE = ' or '
DIFF_CAT_SEPARATE = ';'
NATIONAL_NAME_SEPARATE = ';'
NATIONAL_NAME = 'nation'
NATIONALITY_NFORM = 'noun_nationality'
NATIONALITY_AFORM = 'adj_nationality'


'''
Some string forms need to be filtered in different ways
'''
OTHER_DELETE_SUFFIX = ['stubs']
GENDER_STR_FORM = ['male', 'female', 'women', 'woman']
SPECIAL_STATE_STR_FORM = ['medieval ', 'Medieval ',
                          'ancient ', 'Ancient ',
                          'imperial ', 'Imperial ']
ADDTIONAL_NATIONALITIES = ['African', 'European', 'Asian', 
                           'North American', 'South American',
                           'Antarctic', 'English', 'England']
TEMPORAL_PREFIX = ['-century', '-era', 'dynasty']
MISTAKEN_CATEGORY_STR_FORMS = ['member', 'members', 'people', 'fellow', 'fellows',
                               'academic', 'academics', 'university', 'laureate', 'party' 
                               'school', 'faculty', 'constellation']
OVERLY_EXPLICIT_STR_FORMS = ['scientist']
MISTAKEN_INDEX_STR_FORMS = ['crystallography', 'euclid', 'crystalline solid', 
                            'euclidean solid geometry', 'euclidean geometry',
                            'named after', 'metal', 'constellation', 'glacier',
                            'water ice']