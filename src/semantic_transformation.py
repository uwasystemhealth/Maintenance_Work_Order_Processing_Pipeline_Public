import sys
import pandas as pd
from domain_operations import semantic_transform, tokenization
from generic_operations import print_to_file
import global_variables as v

def semantic_transformation(data_path, sheet_name, columns, short_text_name):
    """Prints corpus with semantic transformation applied"""

    wo_data = pd.read_excel(data_path, sheet_name=sheet_name)
    selected_wo_data = pd.DataFrame(wo_data, columns=["ShortText"])
    short_text_list = selected_wo_data[short_text_name] # just get short text

    # Step 1: Tokenization
    # Generates a token list with punctuation removed
    transformed_text_list = []

    for short_text in short_text_list:
        tokenized = tokenization(short_text)
        new_text = ''
        for token in tokenized:
            new_text += token.lower()
            new_text += ' '

        # Step 2: Semantic Transformation
        # Generates a token list transformed against regex matches
        transformed_text = semantic_transform(new_text)
        transformed_text_list.append(transformed_text)

    # Write output to file
    print_to_file(v.transformed_text_path_stage_1, transformed_text_list, v.transformed_text_heading)


def main():
    print("Starting preprocessor: semantic transformation")
    semantic_transformation(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    print("preprocessor: semantic transformation is complete")
    print('Now run "dictionary-building.py" file')

if __name__ == "__main__":
    main()