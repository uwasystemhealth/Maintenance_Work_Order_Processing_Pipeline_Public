
import pandas as pd
from ast import literal_eval
from generic_operations import print_to_file
import global_variables as v

def spelling_correction():
    """Performs spelling correction on transformed token list"""

    # open preprocessed tokens
    wo_data = pd.read_excel(v.input_file_path_spelling_correction, sheet_name=v.input_file_sheet_name)
    selected_wo_data = pd.DataFrame(wo_data, columns=v.input_file_columns)
    transformed_token_list = list(selected_wo_data[v.input_file_column])

    transformed_stage_1 = stage_1(transformed_token_list)
    transformed_stage_2 = stage_2(transformed_stage_1)
    transformed_stage_3 = stage_3(transformed_stage_2)

    print_to_file(v.transformed_text_path_stage_2, transformed_stage_3, v.transformed_text_heading)


def stage_1(transformed_token_list):
    """Checks tokens against ngram to unigram dictionary"""
    dict_data = pd.read_excel(v.stage_1_input_path, sheet_name=v.input_file_sheet_name)
    selected_correct_token_data = pd.DataFrame(dict_data, columns=v.stage_1_input_file_columns)
    transformed_state_1 = []
    for sentence in transformed_token_list:
        for row in selected_correct_token_data.itertuples():
            b = list(literal_eval(row.ngram))
            ngram = ''
            for word in b: ngram += (' ' + word)
            split_bigram = ngram.strip().split(' ')
            split_sentence = sentence.strip().split(' ')
            if ngram.strip() in sentence and split_bigram[0] in split_sentence and split_bigram[1] in split_sentence:
                sentence = sentence.replace(ngram.strip(), row.unigram)
        transformed_state_1.append(sentence)
    print_to_file(v.stage_1_output_path, transformed_state_1, v.input_file_columns)
    return transformed_state_1


def stage_2(transformed_token_list):
    """Check tokens afaint unigram to ngram dictionary"""
    dict_data = pd.read_excel(v.stage_2_input_path, sheet_name=v.input_file_sheet_name)
    selected_correct_token_data = pd.DataFrame(dict_data, columns=v.stage_2_input_file_columns)
    transformed_stage_2 = []
    for sentence in transformed_token_list:
        for row in selected_correct_token_data.itertuples():
            unigram = row.unigram.strip()
            if unigram in sentence.split(' '):
                sentence = sentence.replace(unigram, row.ngram)
        transformed_stage_2.append(sentence)
    print_to_file(v.stage_2_output_path, transformed_stage_2, v.input_file_columns)
    return transformed_stage_2


def stage_3(transformed_token_list):
    """Check against corrected token dictionary"""
    dict_data = pd.read_excel(v.stage_3_input_path, sheet_name=v.input_file_sheet_name)
    selected_correct_token_data = pd.DataFrame(dict_data, columns=v.stage_3_input_file_columns)
    transformed_state_3 = []
    for sentence in transformed_token_list:
        for row in selected_correct_token_data.itertuples():
            incorrect = row.incorrect.strip()
            if incorrect in sentence.split(' '):
                sentence = sentence.replace(incorrect, row.correct.strip())
        transformed_state_3.append(sentence)
    return transformed_state_3


def main():
    print("Starting preprocessor: spelling correction")
    spelling_correction()
    print("preprocessor: spelling correction is complete")
    print("output: " + v.transformed_text_path_stage_2)
    print('Now run "lemmatisation.py" file')

if __name__ == "__main__":
    main()