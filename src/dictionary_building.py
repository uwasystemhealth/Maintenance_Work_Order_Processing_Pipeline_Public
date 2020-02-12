import pandas as pd
from generic_operations import get_frequent_ngrams, print_to_file
import global_variables as v
import global_parameters as p
import sys
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from  spellchecker import SpellChecker

def dictionary_building(correct_token_list, incorrect_token_list, ngram_to_unigram_dictionary, unigram_to_ngram_dictionary):
    """Prints four dictionaries to support spelling correction"""
    wo_data = pd.read_excel(v.input_file_path_dict_building, sheet_name=v.input_file_sheet_name)
    selected_wo_data = pd.DataFrame(wo_data, columns=v.input_file_columns)
    transformed_token_list = list(selected_wo_data[v.input_file_column])
    build_correct_incorrect_token_dictionaries(transformed_token_list, correct_token_list, incorrect_token_list)
    build_ngram_unigram_dictionaries(transformed_token_list, correct_token_list, incorrect_token_list, ngram_to_unigram_dictionary, unigram_to_ngram_dictionary)


spell = SpellChecker()

def build_correct_incorrect_token_dictionaries(transformed_token_list, correct_token_list, incorrect_token_list):

    for transformed_sentence in transformed_token_list:
        tokens = transformed_sentence.strip().split(' ')
        if " " in tokens:
            tokens.remove(" ")
        correct_token_list.extend(spell.known(tokens))
        incorrect_token_list.extend(spell.unknown(tokens))

    # print correct and incorrect token lists to file
    print_to_file(v.correct_token_dictionary_path, list(set(correct_token_list)), v.correct_token_heading)
    print_to_file(v.incorrect_token_dictionary_path, list(set(incorrect_token_list)), v.incorrect_token_heading)

def build_ngram_unigram_dictionaries(transformed_token_list, correct_token_list, incorrect_token_list, ngram_to_unigram_dictionary, unigram_to_ngram_dictionary):

    ngram_tuples = get_frequent_ngrams(transformed_token_list, p.ngram_occurence_freq)

    for ngram in ngram_tuples:
        merged_ngram = ""
        split_ngram_string = ""
        dash_separated_string = ""
        for t in list(ngram):
            merged_ngram = (merged_ngram + t).strip()
            split_ngram_string = (split_ngram_string + " " + t).strip()
            dash_separated_string = (dash_separated_string + "-" + t).strip()

        # check if the ngram forms a unigram when merged
        if merged_ngram in correct_token_list:
            ngram_to_unigram_dictionary.append([ngram, merged_ngram])
        elif merged_ngram in incorrect_token_list:
            unigram_to_ngram_dictionary.append([merged_ngram, split_ngram_string, dash_separated_string])

    # print to dictionary files
    print_to_file(v.ngram_to_unigram_dictionary_path, ngram_to_unigram_dictionary, v.ngram_to_unigram_headings)
    print_to_file(v.unigram_to_ngram_dictionary_path, unigram_to_ngram_dictionary, v.unigram_to_ngram_headings)

def build_spelling_correction_dict():
    """Compares incorrect token list to correct token list using fuzzywuzzy"""
    corrected_dict = []
    dict_data = pd.read_excel(v.correct_token_dictionary_path, sheet_name=v.input_file_sheet_name)
    correct_token_data = pd.DataFrame(dict_data, columns=v.correct_token_heading)
    correct_token_list = list(correct_token_data[v.correct_token_heading[0]])

    dict_data = pd.read_excel(v.incorrect_token_dictionary_path, sheet_name=v.input_file_sheet_name)
    incorrect_token_data = pd.DataFrame(dict_data, columns=v.incorrect_token_heading)
    incorrect_token_list = list(incorrect_token_data[v.incorrect_token_heading[0]])

    for word in incorrect_token_list:
        if type(word) != float:
            best_guess = process.extractOne(word, correct_token_list)
            print(f"The best match for '{word}' is '{best_guess[0]}' which is a {best_guess[1]}% match.")

            if best_guess[1] > 90:
                corrected_dict.append([word, best_guess[0]])

    print(v.spelling_correction_dictionary_path, corrected_dict, v.spelling_correction_headings)

def main():

    correct_token_list = []
    incorrect_token_list = []
    ngram_to_unigram_dictionary = []
    unigram_to_ngram_dictionary = []

    print("Starting preprocessor: dictionary building")
    dictionary_building(correct_token_list, incorrect_token_list, ngram_to_unigram_dictionary, unigram_to_ngram_dictionary)
    if sys.argv[1] == "1": build_spelling_correction_dict() # long running operation
    print("preprocessor: dictionary building is complete")
    print('Now run "spelling-correction.py" file')

if __name__ == "__main__":
    main()