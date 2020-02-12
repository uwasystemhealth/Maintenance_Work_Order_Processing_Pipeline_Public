import os

# PREPROCESSING
os.system('python3 semantic_transformation.py "../data/static/wo-large.xlsx" "Sheet1" ["ShortText"] "ShortText"')
os.system('python3 dictionary_building.py "1"')
os.system('python3 spelling_correction.py')
os.system('python3 lemmatisation.py')
os.system('python3 abbreviation_correction.py')

# TAGGING
os.system('python3 symptom_state.py')
os.system('python3 maintenance_activity.py')
os.system('python3 maintenance_item.py "1"')

# VALIDATION
os.system('python3 validation_jaccard_index.py')