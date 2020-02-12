import pandas as pd
from generic_operations import print_to_file
import global_variables as v


def abbreviation_correction():

    # open preprocessed tokens
    wo_data = pd.read_excel(v.input_file_path_abbreviation, sheet_name=v.input_file_sheet_name)
    selected_wo_data = pd.DataFrame(wo_data, columns=v.input_file_columns)
    transformed_token_list = list(selected_wo_data[v.input_file_column])

    known_abbreviation_list = [
         ['lh', 'left-hand']
        ,['rh', 'right-hand']
        ,['flh', 'front-left-hand']
        ,['rlh', 'rear-left-hand']
        ,['frh', 'front-right-hand']
        ,['rrh', 'rear-right-hand']
        ,['rr', 'rear-right']
        ,['rl', 'rear-left']
        ,['fr', 'front-right']
        ,['fl', 'front-left']
        , ['rhs', 'right-hand-side']
        , ['lhs', 'left-hand-side']
        , ['hr', 'hour']
        , ['wk', 'week']
    ]

    known_trigram_abbreviation_list = [
        ['u','_', 's', 'unservicable'],
        ['c', '_', 'o', 'changeout'],
        ['d', '_', 's', 'drivers'],
        ['a', '_', 'c', 'air conditioning'],
        ['l', '_', 'h', 'left-hand'],
        ['r', '_', 'h', 'right-hand'],
    ]

    final_sentences = []
    for sentence in transformed_token_list:
        tokens = sentence.split(' ')
        final_tokens = []

        flag = 0
        i = 0

        for index, token in enumerate(tokens):
            final_token = token

            # check if in abbreviation list
            for abbrev, full in known_abbreviation_list:
                if abbrev == token:
                    final_token = full

            # check if in trigram list
            for trigram in known_trigram_abbreviation_list:
                if(index != 0 and index != (len(tokens) - 1) and
                   tokens[index-1] == trigram[0] and tokens[index] == trigram[1] and
                   tokens[index+1] == trigram[2]):
                    final_token = trigram[3]
                    flag = 1
                    i = index
            final_tokens.append(final_token)
        if (flag == 1):
            final_tokens.pop(i+1)
            final_tokens.pop(i-1)
        final_sentences.append(' '.join(final_tokens))
    print_to_file(v.transformed_text_path_stage_4, final_sentences, v.transformed_text_heading)

def main():
    print("Starting preprocessor: abbreviation correction")
    abbreviation_correction()
    print("preprocessor: abbreviation correction is complete")
    print("output: " + v.transformed_text_path_stage_4)
    print('Now run "abbreviation-correction.py" file')

if __name__ == "__main__":
    main()


