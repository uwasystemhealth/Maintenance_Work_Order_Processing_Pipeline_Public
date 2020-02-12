
import os

# INSTALL
os.system('py -m pip install pandas')
os.system('py -m pip install pattern')
os.system('py -m pip install nltk')
os.system('py -m pip install gensim')
os.system('py -m pip install fuzzywuzzy')
os.system('py -m pip install pyspellchecker')
os.system('py -m pip install xlrd')
os.system('py -m pip install openpyxl')

# PREPROCESSING
os.system('py semantic_transformation.py "../data/static/wo-large.xlsx" "Sheet1" ["ShortText"] "ShortText"')
os.system('py dictionary_building.py "1"')
os.system('py spelling_correction.py')
os.system('py lemmatisation.py')
os.system('py abbreviation_correction.py')

# TAGGING
os.system('py symptom_state.py')
os.system('py maintenance_activity.py')
os.system('py maintenance_item.py "1"')

# VALIDATION
os.system('py validation_jaccard_index.py')
