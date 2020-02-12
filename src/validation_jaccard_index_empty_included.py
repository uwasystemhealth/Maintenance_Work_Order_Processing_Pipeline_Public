import pandas as pd
import global_variables as v

def validation(manually_tagged_rows, automatically_tagged_rows, delimiter):

     correct = 0
     incorrect = 0
     ignored = 0
     final_jaccard_index = 0
     jaccard_count = 0
     recordCount = 0
     zeroTaggedCount = 0;

     for index, row in manually_tagged_rows.iterrows(): # for each manually tagged record

        #print(row)
        true_tokens = row['tagged_record'].split(' ')
        row_number = row['row_number']

        final_tokens = []
        generated_tokens = []

        for true_token in true_tokens:
            if delimiter in true_token:  # if something is tagged as symptom/state
                true_token = true_token.replace('-', ' ') # remove punctuation from results
                true_token = true_token.replace(delimiter, ' ') # remove delimiter from results
                final_tokens.append(true_token.strip())

        test_tokens = automatically_tagged_rows.iloc[row_number - 1] # get the corresponding auto tagged record
        test_tokens = test_tokens['tagged_sentence'].split(' ')

        for test_token in test_tokens:
            if delimiter in test_token:
                test_token = test_token.replace('-', ' ') # remove punctuation from results
                test_token = test_token.replace(delimiter, ' ') # remove delimiter from results
                generated_tokens.append(test_token.strip())

        if len(final_tokens) == 0 :
            ignored += 1
        elif final_tokens == generated_tokens:
            correct += 1
        else:
            incorrect += 1
            #print('true' + str(final_tokens))
            #print('attempt' + str(generated_tokens))
            #print (true_tokens)

        common_phrases = list(set(final_tokens).intersection(generated_tokens))
        # print("common: " + str(common_phrases))
        all_phrases = list(set(final_tokens + generated_tokens))
        # print("all: " + str(all_phrases))

        if (len(all_phrases) == 0 and len(common_phrases) == 0):
            jaccard_count = jaccard_count + 1
            zeroTaggedCount = zeroTaggedCount + 1;
        else:
            jaccard_count = jaccard_count + len(common_phrases)/len(all_phrases)
        recordCount = recordCount + 1


     print('correct:')
     print(correct)
     print('incorrect:')
     print(incorrect)
     print('% correct:')
     print((correct/(incorrect+correct))*100)

     final_jaccard_index = jaccard_count/recordCount
     print('jaccard_index:')
     print(final_jaccard_index)
     print(zeroTaggedCount)


manually_tagged_data = pd.read_excel(v.validation_path, sheet_name=v.input_file_sheet_name)

def main():

    print("Starting Pipeline Validation")

    print("Validating Symptom/State Tagged Records") # 82%   # JI:0.823
    data = pd.read_excel(v.symptom_state_output_path, sheet_name=v.input_file_sheet_name)
    validation(manually_tagged_data, data, v.symptom_state_tag_symbol)

    print("Validating Maintenance Activity Tagged Records") # 86%   # JI:0.897
    data = pd.read_excel(v.maintenance_activity_output_path, sheet_name=v.input_file_sheet_name)
    validation(manually_tagged_data, data, v.maintenance_activity_tag_symbol)

    print("Validating Maintenance Item Tagged Records") # 34%   # JI:0.359
    data = pd.read_excel(v.maintenance_item_output_path, sheet_name=v.input_file_sheet_name)
    validation(manually_tagged_data, data, v.maintenance_item_tag_symbol)

    ### Baseline validation
    print("Validating Symptom/State Tagged Records") # 82%
    print(v.baseline_output_path)
    data = pd.read_excel(v.baseline_output_path, sheet_name=v.input_file_sheet_name)
    print('here')
    validation(manually_tagged_data, data, v.symptom_state_tag_symbol)

    print("Validating Maintenance Activity Tagged Records") # 69%
    data = pd.read_excel(v.baseline_output_path, sheet_name=v.input_file_sheet_name)
    validation(manually_tagged_data, data, v.maintenance_activity_tag_symbol)

    print("Validating Maintenance Item Tagged Records") # 24%
    data = pd.read_excel(v.baseline_output_path, sheet_name=v.input_file_sheet_name)
    validation(manually_tagged_data, data, v.maintenance_item_tag_symbol)

    print("Validation Finished")

if __name__ == "__main__":
    main()