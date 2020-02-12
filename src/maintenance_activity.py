
import pandas as pd
from pattern.en import conjugate
import global_variables as v
from generic_operations import print_to_file

def detect_activities(transformed_text_list, dictionary_list):

    tagged_records = []

    try: conjugate('hello', 'inf') # dirty fix to python 3.7 / pattern error
    except: pass

    for sentence in transformed_text_list:
        if type(sentence) != float: # skip if nan?
            tokens = sentence.split(' ')
            for idx, token in enumerate(tokens):
                if v.symptom_state_tag_symbol not in token: # if it has not already been tagged as a symptom/state
                    conjugated_current_word = conjugate(token, 'inf')
                    if conjugated_current_word in dictionary_list:
                        tokens[idx] = token + v.maintenance_activity_tag_symbol
            tagged_records.append(' '.join(tokens))
        else:
            tagged_records.append('')

    print_to_file(v.maintenance_activity_output_path, tagged_records, v.output_headings)

def main():
    print("Starting tagging: maintenance_activity")

    preprocessed_data = pd.read_excel(v.symptom_state_output_path, sheet_name=v.input_file_sheet_name)
    selected_data = pd.DataFrame(preprocessed_data, columns=v.output_headings)
    transformed_text_list = list(selected_data[v.output_heading])

    dict_data = pd.read_excel(v.maint_activity_dict_path, sheet_name=v.input_file_sheet_name)
    selected_data = pd.DataFrame(dict_data, columns=v.dictionary_headings)
    dictionary_list = list(selected_data[v.dictionary_heading])

    detect_activities(transformed_text_list, dictionary_list)

    print("tagging: maintenance activity tagging is complete")
    print('Now run "maintenance_item.py" file')

if __name__ == "__main__":
    main()
