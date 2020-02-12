from generic_operations import get_frequent_ngrams
import pandas as pd
from nltk.util import ngrams
from generic_operations import print_to_file
import math
import global_parameters as p
import global_variables as v

# save file of frequency n-grams
def ngram_detection(text_list):
    ngrams = get_frequent_ngrams(text_list, p.ngram_occurence_freq)
    print_to_file(v.all_frequent_ngrams_path, ngrams, v.ngrams_headings)

# save filtered n-grams as file
def keyword_based_ngram_filtering():
    filtered_ngrams = []
    headwords = ['cannot', 'not', 'is', 'are']
    ngram_data = pd.read_excel(v.all_frequent_ngrams_path, sheet_name=v.input_file_sheet_name)
    df = pd.DataFrame(ngram_data, columns=v.ngrams_headings)
    for index, row in df.iterrows():
        if row['headword'] != '' and row['headword'] in headwords:

            filtered_ngrams.append([row['headword'], row['tailword1'],
                                    row['tailword2'], row['tailword3'], row['tailword4'], row['tailword5']])
        if row['headword'] == 'to' and row['tailword1'] == 'be':
            filtered_ngrams.append([row['headword'], row['tailword1'],
                                    row['tailword2'], row['tailword3'], row['tailword4']])
    print_to_file(v.symptom_state_filtered_ngrams_path, filtered_ngrams, v.ngrams_headings)

def dictionary_building():
    symptom_state_dictionary = []
    # step 1: get filtered ngrams and append to dictionary
    n_data = pd.read_excel(v.symptom_state_filtered_ngrams_path, sheet_name=v.input_file_sheet_name)
    df = pd.DataFrame(n_data, columns=v.ngrams_headings)
    for index, row in df.iterrows():
        row['headword'] = get_proper_string(row['headword'])
        row['tailword1'] = get_proper_string(row['tailword1'])
        row['tailword2'] = get_proper_string(row['tailword2'])
        row['tailword3'] = get_proper_string(row['tailword3'])
        row['tailword4'] = get_proper_string(row['tailword4'])
        row['tailword5'] = get_proper_string(row['tailword5'])

        symptom_state_dictionary.append((row['headword'] + ' ' + row['tailword1'] + ' ' +
                                             row['tailword2'] + ' '+row['tailword3']+
                                             ' ' +row['tailword4']+' '+row['tailword5']).strip())

        # step 2: append tailwords to dictionary if headword is "is" or "are"
        if row['headword'] == "is" or row['headword'] == "are":
            words = (row['tailword1'] + ' ' +
             row['tailword2'] + ' ' + row['tailword3'] +
             ' ' + row['tailword4'] + ' ' + row['tailword5']).strip()
            symptom_state_dictionary.append(words)

    # step 3: append additional describing nouns to dictionary
    symptom_state_dictionary.append('problem')
    symptom_state_dictionary.append('error')
    symptom_state_dictionary.append('leak')
    symptom_state_dictionary.append('fault')
    symptom_state_dictionary.append('damage')
    symptom_state_dictionary.append('failure')

    print_to_file(v.symptom_state_dictionary_path, symptom_state_dictionary, v.dictionary_headings)

# save symptom / state tagged records
def tagging(transformed_text_list):
    tagged_records = []
    dictionary_data = pd.read_excel(v.symptom_state_dictionary_path, sheet_name=v.input_file_sheet_name)
    dictionary_df = pd.DataFrame(dictionary_data, columns=v.dictionary_headings)
    dictionary_list = []
    for index, row in dictionary_df.iterrows():
        dictionary_list.append(row['words'].split(' '))

    for sentence in transformed_text_list:
        tokens = sentence.strip().split(' ')
        total_ngrams = []
        for n in range(2, 7): total_ngrams = total_ngrams + list(ngrams(tokens, n))
        tagged, flag = tag_record(tokens, total_ngrams, dictionary_list)

        # else if single term matches then tag
        # case 1: single term from describing nouns
        # case 2: single term from dictionary
        if (flag == 0):
            for index, token in enumerate(tokens):
                for row in dictionary_list:
                    if len(row) == 1 and token == row[0] and len(token) > 3:
                        tokens[index] = token + v.symptom_state_tag_symbol

        if (flag == 1):
            joined = ''.join(w if (w.endswith(v.symptom_state_tag_symbol) and (i - 1 != len(tagged) and tagged[i].endswith(v.symptom_state_tag_symbol))) else w + ' ' for i, w in enumerate(tagged)).lstrip()
            tagged_records.append(joined)
        else:
            tagged_records.append(' '.join(tokens))

    print_to_file(v.symptom_state_output_path, tagged_records, v.output_headings)

def get_proper_string(str):
    try:
        if math.isnan(str): return ' '
        return str
    except:
        return str

def tag_record(tokens, total_ngrams, dictionary_list):
    for found_ngram in total_ngrams:
        for dictionary_ngram in dictionary_list:
            if (list(found_ngram) == dictionary_ngram):
                for index, token in enumerate(tokens):
                    if (token in found_ngram):
                        tokens[index] = token + v.symptom_state_tag_symbol
                return tokens, 1
    return tokens, 0


def main():
    print("Starting tagging: symptom_state")

    preprocessed_data = pd.read_excel(v.transformed_text_path_stage_4, sheet_name=v.input_file_sheet_name)
    selected_data = pd.DataFrame(preprocessed_data, columns=v.input_file_columns)
    transformed_text_list = list(selected_data[v.input_file_column])

    ngram_detection(transformed_text_list)
    keyword_based_ngram_filtering()
    dictionary_building()
    tagging(transformed_text_list)

    print("tagging: symptom state tagging is complete")
    print('Now run "maintenance_activity.py" file')

if __name__ == "__main__":
    main()
