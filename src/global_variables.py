
# COMMON
transformed_text_heading = ["transformedtokens"]
input_file_sheet_name = 0
input_file_columns = ['transformedtokens']
input_file_column = 'transformedtokens'
transformed_text_path_stage_4 = "../data/fluid/preprocessed-text-list-stage-4.xlsx"
symptom_state_output_path = "../data/fluid/output-symptom-state.xlsx"
maintenance_activity_output_path = "../data/fluid/output-activity.xlsx"
maintenance_item_output_path = "../data/fluid/output-maintenance-item.xlsx"
output_headings = ["tagged_sentence"]
output_heading = "tagged_sentence"
dictionary_headings = ["words"]
dictionary_heading = "words"
all_frequent_ngrams_path = "../data/fluid/frequent-ngrams.xlsx"
all_tagged_frequent_ngrams_path = "../data/fluid/frequent-tagged-ngrams.xlsx"
ngrams_headings = ['headword','tailword1', 'tailword2', 'tailword3', 'tailword4', 'tailword5']
symptom_state_tag_symbol = '#'
maintenance_activity_tag_symbol = '='
maintenance_item_tag_symbol = '~'

# SEMANTIC TRANSFORMATION
transformed_text_path_stage_1 = "../data/fluid/preprocessed-text-list-stage-1.xlsx"

# DICTIONARY BUILDING
input_file_path_dict_building = "../data/fluid/preprocessed-text-list-stage-1.xlsx"
correct_token_dictionary_path = "../data/fluid/correct-token-dictionary.xlsx"
incorrect_token_dictionary_path = "../data/fluid/incorrect-token-dictionary.xlsx"
ngram_to_unigram_dictionary_path = "../data/fluid/ngram-to-unigram-dictionary.xlsx"
unigram_to_ngram_dictionary_path = "../data/fluid/unigram-to-ngram-dictionary.xlsx"
spelling_correction_dictionary_path = "../data/fluid/spelling-correction-dictionary.xlsx"
correct_token_heading = ["correcttokens"]
incorrect_token_heading = ["incorrecttokens"]
ngram_to_unigram_headings = ["ngram", "unigram"]
unigram_to_ngram_headings = ["unigram", "ngram", "ngram2"]
spelling_correction_headings = ['incorrect', 'correct']

# SPELLING_CORRECTION
input_file_path_spelling_correction = "../data/fluid/preprocessed-text-list-stage-1.xlsx"
stage_1_input_path = "../data/fluid/ngram-to-unigram-dictionary.xlsx"
stage_1_input_file_columns = ["ngram", "unigram"]
stage_1_output_path = "../data/fluid/spelling-correction-stage-1.xlsx"
stage_2_input_path = "../data/fluid/unigram-to-ngram-dictionary.xlsx"
stage_2_input_file_columns = ["unigram", "ngram", "ngram2"]
stage_2_output_path = "../data/fluid/spelling-correction-stage-2.xlsx"
stage_3_input_path = "../data/fluid/spelling-corrected-dictionary.xlsx"
stage_3_input_file_columns = ["incorrect", "correct"]
transformed_text_path_stage_2 = "../data/fluid/preprocessed-text-list-stage-2.xlsx"

# LEMMATISATION
input_file_path_lemmatisation = "../data/fluid/preprocessed-text-list-stage-2.xlsx"
transformed_text_path_stage_3 = "../data/fluid/preprocessed-text-list-stage-3.xlsx"

#ABBREVIATION CORRECTION
input_file_path_abbreviation = "../data/fluid/preprocessed-text-list-stage-3.xlsx"

# SYMPTOM STATE
symptom_state_filtered_ngrams_path = "../data/fluid/symptom_state_filtered_ngrams.xlsx"
symptom_state_dictionary_path = "../data/fluid/dictionary_symptom_state.xlsx"

# MAINTENANCE ACTIVITY
maint_activity_dict_path = '../data/static/maintenance-activity-dict.xlsx'

# MAINTENANCE ITEM
maint_item_filtering_stage_1_path = '../data/fluid/maintenance-item-stage-1.xlsx'
maint_item_filtering_stage_2_path = '../data/fluid/maintenance-item-stage-2.xlsx'
word_2_vec_model_path = '../data/fluid/input-output-word2vec-model'
maint_item_static_dictionary_path = '../data/static/maintenance-item-dict.xlsx'
maintenance_item_tagging_1 = '../data/fluid/maintenance-item-output-stage-1.xlsx'
maintenance_item_tagging_2 = '../data/fluid/maintenance-item-output-stage-2.xlsx'

# BASELINE
baseline_output_path = "../data/fluid/baseline-output.xlsx"

# VALIDATION
# validation_path = "../data/static/manually_tagged_records.xlsx"
validation_path = "../data/static/manually_tagged_records_mh.xlsx"