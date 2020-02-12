import pandas as pd
import global_variables as v
import statistics

def run_word_counter(preprocessed_rows):

    count_list = []

    for index, row in preprocessed_rows.iterrows():  # for each record in data file
        tokens = row['transformedtokens'].strip().split(' ')
        print(tokens)

        token_count = len(tokens)
        count_list.append(token_count)

    print('maximum length: ' + str(max(count_list)))
    print('mean no. of words: ' + str(sum(count_list) / len(count_list) ))
    print('standard deviation ' + str(statistics.stdev(count_list)))

def main():

    print("Starting Pipeline Validation")

    print("Validating Maintenance Item Tagged Records")
    data = pd.read_excel(v.transformed_text_path_stage_4, sheet_name=v.input_file_sheet_name)
    run_word_counter(data)

    print("Validation Finished")

if __name__ == "__main__":
    main()