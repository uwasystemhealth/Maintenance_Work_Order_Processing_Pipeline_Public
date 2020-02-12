
import pandas as pd
from generic_operations import print_to_file
import global_variables as v
import nltk
from nltk.translate.ribes_score import position_of_ngram

def baseline_tagging(transformed_text_list):

    tagged_records = [];
    for sentence in transformed_text_list:

        s = sentence.strip().split(" ")

        flag = False
        while flag is False:
            if '' in s:
                s.remove('')
            if '' not in s:
                flag = True

        # regular expression used for noun phrase chunking
        grammar = "NP: {<NN.*>*}"
        cp = nltk.RegexpParser(grammar)

        # tagged_s is a list of tuples consisting of the word and its pos tag
        if '+' not in s:
            tagged_s = nltk.pos_tag(s)
            for c, word_pos_tag_tuple in enumerate(tagged_s):
                word, pos_tag = word_pos_tag_tuple
                # only searching for the original verb
                if 'VB' in pos_tag:
                    s[c] = word + '='
                elif 'JJ' in pos_tag:
                    s[c] = word + '#'

            #noun phrase chunking for items detection
            result = cp.parse(tagged_s)
            for subtree in result.subtrees():
                if subtree.label() == 'NP':
                    t = subtree
                    noun_phrase_chunk = ' '.join(word for word, pos in t.leaves())
                    tagged_noun_phrase_chunk = '~'.join(word for word, pos in t.leaves())
                    starting_index_noun_phrase_chunk = position_of_ngram(tuple(noun_phrase_chunk.split()), s)
                    s[starting_index_noun_phrase_chunk] = tagged_noun_phrase_chunk
                    for i in range(1, len(t.leaves())):
                        s[starting_index_noun_phrase_chunk + i] = ''

            s = [x for x in s if x]
            string_to_print = ' '.join(s)
            tagged_records.append(string_to_print)
        else:
            string_to_print = ' '.join(s)
            tagged_records.append(string_to_print)

    print_to_file(v.baseline_output_path, tagged_records, v.output_headings)

def main():
    print("Starting tagging: baseline")

    preprocessed_data = pd.read_excel(v.transformed_text_path_stage_4, sheet_name=v.input_file_sheet_name)
    selected_data = pd.DataFrame(preprocessed_data, columns=v.input_file_columns)
    transformed_text_list = list(selected_data[v.input_file_column])

    baseline_tagging(transformed_text_list);

    print("tagging: baseline tagging is complete")
    print('Now run "validation.py" file')

if __name__ == "__main__":
    main()
