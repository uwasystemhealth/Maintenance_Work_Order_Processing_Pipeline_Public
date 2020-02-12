from nltk.stem.wordnet import WordNetLemmatizer
Lem = WordNetLemmatizer()
import pandas as pd
from generic_operations import print_to_file
import global_variables as v

def lemmatisation():

    # open preprocessed tokens
    wo_data = pd.read_excel(v.input_file_path_lemmatisation, sheet_name=v.input_file_sheet_name)
    selected_wo_data = pd.DataFrame(wo_data, columns=v.input_file_columns)
    transformed_token_list = list(selected_wo_data[v.input_file_column])

    # create list of tokens
    token_list = []
    for sentence in transformed_token_list:
        tokens = sentence.split(' ')
        for token in tokens:
            token_list.append(token)

    token_set = list(set(token_list))
    final_sentences = []
    for sentence in transformed_token_list:
        tokens = sentence.split(' ')
        final_tokens = []
        for w in tokens:
            final_word = w
            lemmatized_word = Lem.lemmatize(w)
            if len(w) > 3 and lemmatized_word != w:
                if lemmatized_word in tokens:
                    final_word = lemmatized_word
                elif len(w) > 4 and w[-1] == 's' and w[:-1] in token_set:
                    final_word = lemmatized_word
            final_tokens.append(final_word)
        final_sentences.append(' '.join(final_tokens))
    print_to_file(v.transformed_text_path_stage_3, final_sentences, v.transformed_text_heading)


def main():
    print("Starting preprocessor: lemmatisation")
    lemmatisation()
    print("preprocessor: lemmatisation is complete")
    print("output: " + v.transformed_text_path_stage_3)
    print('Now run "abbreviation-correction.py" file')

if __name__ == "__main__":
    main()