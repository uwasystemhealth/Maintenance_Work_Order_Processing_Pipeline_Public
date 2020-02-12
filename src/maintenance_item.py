
import pandas as pd
import math
from generic_operations import get_frequent_ngrams, create_word2vec_model, ngrams, print_to_file, get_proper_string
from nltk.corpus import stopwords
import gensim
from collections import defaultdict
import nltk
import global_variables as v
import global_parameters as p
import sys

def stage_1():
    '''Filter out all ngrams that contain a symptom/state, maint activity or stopwords'''
    filtered_ngrams = []

    # Get frequent ngrams
    ngram_data = pd.read_excel(v.all_tagged_frequent_ngrams_path, sheet_name=v.input_file_sheet_name)


    frequent_ngram_data = pd.DataFrame(ngram_data, columns=v.ngrams_headings)

    # Filter ngrams
    stop_words = stopwords.words('english')
    stop_words = stop_words + ['right', 'left', 'front', 'rear', 'top', 'bottom', 'right-hand', 'left-hand', 'hand',
                               'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'hour', 'day', 'week', 'month', 'year']

    # get incorrect token list
    dict_data = pd.read_excel(v.incorrect_token_dictionary_path, sheet_name=v.input_file_sheet_name)
    incorrect_token_data = pd.DataFrame(dict_data, columns=v.incorrect_token_heading)
    incorrect_token_list = list(incorrect_token_data[v.incorrect_token_heading[0]])

    for index, row in frequent_ngram_data.iterrows():
        row['headword'] = get_proper_string(row['headword'])
        row['tailword1'] = get_proper_string(row['tailword1'])
        row['tailword2'] = get_proper_string(row['tailword2'])
        row['tailword3'] = get_proper_string(row['tailword3'])
        row['tailword4'] = get_proper_string(row['tailword4'])
        row['tailword5'] = get_proper_string(row['tailword5'])

        combined = (row['headword'] + ' ' + row['tailword1'] + ' ' +
                                             row['tailword2'] + ' '+row['tailword3']+
                                             ' ' +row['tailword4']+' '+row['tailword5']).strip()

        if (v.symptom_state_tag_symbol not in combined) and (v.maintenance_activity_tag_symbol not in combined):
            # if the record in not a symptom or an activity (or already tagged as a maintenance item

            combined_tokens = combined.split()
            found_flag = 0
            # check if contains "common stopwords"
            for token in combined_tokens:
                if token in stop_words or token in incorrect_token_list:
                    found_flag = 1

            if (found_flag == 0):
                filtered_ngrams.append(combined_tokens)

    print_to_file(v.maint_item_filtering_stage_1_path, filtered_ngrams, ['headword','tailword1', 'tailword2', 'tailword3', 'tailword4', 'tailword5'])

def stage_2():
    '''Filter outlier words with word2vec'''

    outlier_words_dict = defaultdict(int)
    outlier_words_pos_filtered_dict = defaultdict(int)
    single_word_freq_dict = defaultdict(int)

    # get maintenance item dict
    ngram_data = pd.read_excel(v.maint_item_filtering_stage_1_path, sheet_name=v.input_file_sheet_name)
    maintenance_items = pd.DataFrame(ngram_data, columns=v.ngrams_headings)

    # get preprocessed maitenance records
    preprocessed_data = pd.read_excel(v.transformed_text_path_stage_4, sheet_name=v.input_file_sheet_name)
    selected_data = pd.DataFrame(preprocessed_data, columns=v.input_file_columns)
    transformed_text_list = list(selected_data[v.input_file_columns])

    # get generated model
    model = gensim.models.Word2Vec.load(v.word_2_vec_model_path )

    for index, row in maintenance_items.iterrows():

        row['headword'] = get_proper_string(row['headword'])
        row['tailword1'] = get_proper_string(row['tailword1'])
        row['tailword2'] = get_proper_string(row['tailword2'])
        row['tailword3'] = get_proper_string(row['tailword3'])
        row['tailword4'] = get_proper_string(row['tailword4'])
        row['tailword5'] = get_proper_string(row['tailword5'])

        combined = (row['headword'] + ' ' + row['tailword1'] + ' ' +
                                                 row['tailword2'] + ' '+row['tailword3']+
                                                 ' ' +row['tailword4']+' '+row['tailword5']).strip()

        parts_list = combined.split(' ')
        number_of_parts = len(parts_list)


        for a in parts_list:

            #print(parts_list)

            single_word_freq_dict[a] += 1

            if a not in model.wv.vocab:
                number_of_parts -= 1

        if number_of_parts == 0:
            outlier_word = ''
            pos = ''
            dist_mean = 0
        else:
            outlier_word , dist_mean = customized_doesnt_match(model.wv, parts_list)
            outlier_words_dict[outlier_word] += 1
            outlier_words_pos_filtered_dict[outlier_word] += 1

    outlier_words_pos_filtered_dic_ranked_by_ratio = {}
    outlier_words_ratio_2 = {}
    for item in outlier_words_dict:
        freq, ratio = 0, 0
        if item in single_word_freq_dict:
            freq = single_word_freq_dict[item]
            ratio_unfiltered = outlier_words_dict[item] / freq
            ratio = outlier_words_pos_filtered_dict[item] / freq
        outlier_words_pos_filtered_dic_ranked_by_ratio[item] = ratio
        outlier_words_ratio_2[item] = ratio_unfiltered

    ratio_threshold = 0.8
    stopwords_stage_2 = [a for a in outlier_words_pos_filtered_dic_ranked_by_ratio if outlier_words_pos_filtered_dic_ranked_by_ratio[a] > ratio_threshold]
    print(stopwords_stage_2)

    final = []

    for index, row in maintenance_items.iterrows():

        row['headword'] = get_proper_string(row['headword'])
        row['tailword1'] = get_proper_string(row['tailword1'])
        row['tailword2'] = get_proper_string(row['tailword2'])
        row['tailword3'] = get_proper_string(row['tailword3'])
        row['tailword4'] = get_proper_string(row['tailword4'])
        row['tailword5'] = get_proper_string(row['tailword5'])

        combined = (row['headword'] + ' ' + row['tailword1'] + ' ' +
                        row['tailword2'] + ' ' + row['tailword3'] +
                        ' ' + row['tailword4'] + ' ' + row['tailword5']).strip()

        found = 0;
        combined_list = [row['headword'], row['tailword1'], row['tailword2'], row['tailword3'], row['tailword4'], row['tailword5']]

        for stopword in stopwords_stage_2:
            if stopword in combined_list:
                print(combined_list)
                found = 1;

        if found == 0:
            final.append(combined)

    print_to_file(v.maint_item_filtering_stage_2_path, final, v.dictionary_headings);

def tagging(transformed_text_list):

    tagged_records = []

    # check against fluid dicitionay
    dictionary_data = pd.read_excel(v.maint_item_filtering_stage_2_path, sheet_name=v.input_file_sheet_name)
    dictionary_df = pd.DataFrame(dictionary_data, columns=v.dictionary_headings)

    dictionary_list = []
    for index, row in dictionary_df.iterrows():
        dictionary_list.append(row['words'].split(' '))

    counter = 0;
    for sentence in transformed_text_list:
        counter = counter + 1;
        #print(counter)

        if type(sentence) != float:

            tokens = sentence.strip().split(' ')
            total_ngrams = []
            for n in range(7, 1, -1): total_ngrams = total_ngrams + list(
                ngrams(tokens, n))  ## REVERSE SO THAT LONGER N-GRAMS TAGGED FIRST
            tagged, flag = tag_record(tokens, total_ngrams, dictionary_list)

            # else if single term matches then tag
            if (flag == 0):
                for index, token in enumerate(tokens):
                    for row in dictionary_list:
                        if len(row) == 1 and token == row[0]:
                            tokens[index] = token + v.maintenance_item_tag_symbol

            if (flag == 1):
                joined = ''.join(
                    w if (w.endswith(v.maintenance_item_tag_symbol)) else w + ' ' for i, w in
                    enumerate(tagged)).lstrip()

                tagged_records.append(joined)

                print(joined)

            else:
                tagged_records.append(' '.join(tokens))
        else:
            tagged_records.append('')

    print_to_file(v.maintenance_item_tagging_1, tagged_records, v.output_headings)

    tagged_records = []

    preprocessed_data = pd.read_excel(v.maintenance_item_tagging_1, sheet_name=v.input_file_sheet_name)
    selected_data = pd.DataFrame(preprocessed_data, columns=v.output_headings)
    transformed_text_list = list(selected_data[v.output_heading])

    # check against static dictionary
    print('step 2 begin')
    dictionary_data_static = pd.read_excel(v.maint_item_static_dictionary_path, sheet_name=v.input_file_sheet_name)
    dictionary_df_static = pd.DataFrame(dictionary_data_static, columns=['words'])

    dictionary_list = []
    for index, row in dictionary_df_static.iterrows():
        dictionary_list.append(row['words'].split(' '))

    counter = 0;
    for sentence in transformed_text_list:
        counter = counter+1;
        #print(counter)

        if type(sentence) != float:

            tokens = sentence.strip().split(' ')
            total_ngrams = []
            for n in range(7, 1, -1): total_ngrams = total_ngrams + list(ngrams(tokens, n)) ## REVERSE SO THAT LONGER N-GRAMS TAGGED FIRST
            tagged, flag = tag_record(tokens, total_ngrams, dictionary_list)

            # else if single term matches then tag
            if (flag == 0):
                for index, token in enumerate(tokens):
                    for row in dictionary_list:
                        if len(row) == 1 and token == row[0]:
                            tokens[index] = token + v.maintenance_item_tag_symbol
                            #print(token)
            if (flag == 1):
                joined = ''.join(
                    w if (w.endswith(v.maintenance_item_tag_symbol)) else w + ' ' for i, w in
                    enumerate(tagged)).lstrip()
                tagged_records.append(joined)
                #print(joined)
            else:
                tagged_records.append(' '.join(tokens))
        else:
            tagged_records.append('')

    #print(tagged_records)

    print_to_file(v.maintenance_item_tagging_2, tagged_records, v.output_headings)

    # combine tags
    tagged_records = []

    print('step 3 begin')
    counter = 0;

    preprocessed_data = pd.read_excel(v.maintenance_item_tagging_2, sheet_name=v.input_file_sheet_name)
    selected_data = pd.DataFrame(preprocessed_data, columns=v.output_headings)
    transformed_text_list  = list(selected_data[v.output_heading])


    for sentence in transformed_text_list:

        counter = counter+1
        #print(counter)

        if type(sentence) != float:

            tagged_sentence = ''
            tokens = sentence.strip().split(' ')

            #print(tokens)
            i = 0
            while i <= len(tokens) - 1:
                if i != 0 and (v.maintenance_item_tag_symbol in tokens[i]) and (v.maintenance_item_tag_symbol in tokens[i-1]): # check backward
                    #print('herexx')
                    print(tokens)
                    if (tokens[i].endswith('~')):
                        tokens[i-1]=tokens[i-1]+tokens[i]
                    else:
                        tokens[i-1] = tokens[i-1] + '~' + tokens[i]
                    del tokens[i]

                    if i == len(tokens) - 1:
                        i = i + 1;

                    #print('here3');
                elif i != len(tokens) - 1 and tokens[i].endswith(v.maintenance_item_tag_symbol) and (v.maintenance_item_tag_symbol in tokens[i+1]):
                    #print('here1')
                    tokens[i] = tokens[i]+tokens[i+1]
                    del tokens[i+1]
                    i = i + 1;
                elif i != len(tokens) -1 and (v.maintenance_item_tag_symbol in tokens[i+1]) and (v.maintenance_item_tag_symbol in tokens[i]):
                    #print('here2')
                    tokens[i] = tokens[i]+'~'+tokens[i+1]
                    del tokens[i + 1]
                    #print(tokens[i])
                    i = i + 1;
                else:
                    i = i+1;

                #if (i == len(tokens)):
                #    i = i-1;
                #remove last word tag if ngram
                if i != len(tokens) and tokens[i].count('~') > 1 and tokens[i].endswith('~'):
                    tokens[i] = tokens[i][:-1]

            #(tokens)
            joined = ' '.join(tokens).lstrip()
            #print(joined)


            tagged_records.append(joined)

        else:
            tagged_records.append('+')

    #print(tagged_records)

    print_to_file(v.maintenance_item_output_path, tagged_records, v.output_headings)

def get_next(list, i):
    try:
        element = list[i+1]
        return True
    except:
        return False

def customized_doesnt_match(word_Embeddings_Keyed_Vectors, words):
    from numpy import dot,vstack,float32 as REAL
    from gensim import matutils
    word_Embeddings_Keyed_Vectors.init_sims()
    used_words = [word for word in words if word in word_Embeddings_Keyed_Vectors]
    if len(used_words) != len(words):
        ignored_words = set(words) - set(used_words)
        print("vectors for words_by_alphebat %aspell_checker are not present in the model, ignoring these words_by_alphebat", ignored_words)
    if not used_words:
        raise ValueError("cannot select a word from an empty list")
    vectors = vstack(word_Embeddings_Keyed_Vectors.word_vec(word, use_norm=True) for word in used_words).astype(REAL)
    mean = matutils.unitvec(vectors.mean(axis=0)).astype(REAL)
    dists = dot(vectors, mean)
    dists_mean = dists.mean(axis=0)
    return sorted(zip(dists, used_words))[0][1],dists_mean

def generate_word_embeddings():
    create_word2vec_model()

def tag_record(tokens, total_ngrams, dictionary_list):

    for found_ngram in total_ngrams:
        for dictionary_ngram in dictionary_list:
            if (list(found_ngram) == dictionary_ngram):
                for index, token in enumerate(tokens):
                    if (token in found_ngram
                        and (get_next(tokens, index)
                        and tokens[index+1] in found_ngram)
                        ):
                        tokens[index] = token + '~'
                return tokens, 1
    return tokens, 0


def main():
    print("Starting tagging: maintenance_item")

    preprocessed_data = pd.read_excel(v.maintenance_activity_output_path, sheet_name=v.input_file_sheet_name)
    selected_data = pd.DataFrame(preprocessed_data, columns=v.output_headings)
    transformed_text_list = list(selected_data[v.output_heading])

    ngrams = get_frequent_ngrams(transformed_text_list, p.ngram_occurence_freq)
    print_to_file(v.all_tagged_frequent_ngrams_path, ngrams, v.ngrams_headings)

    stage_1()
    print("stage 1 complete")
    if sys.argv[1] == "1": generate_word_embeddings() # long running operation
    stage_2()
    print("stage 2 complete")
    tagging(transformed_text_list)

    print("tagging: maintenance item tagging is complete")
    print('THE PROCESSING PIPELINE HAS COMPLETED SUCCESSFULLY')

if __name__ == "__main__":
    main()
