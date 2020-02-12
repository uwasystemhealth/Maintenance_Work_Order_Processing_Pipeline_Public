
from collections import Counter
from nltk.util import ngrams
import gensim
import pandas as pd
import math
import global_variables as v

def get_frequent_ngrams(token_list, occurence_frequency):
    bigram_tuples = []
    full_ngrams_list = []
    for row in token_list:
        if (type(row) != float):
            tokens = [token for token in row.split(" ") if token != ""]

            # get ngrams - 2
            bigrams = list(ngrams(tokens, 2))
            for found in bigrams:
                full_ngrams_list.append(found)

            # get ngrams - 3
            bigrams = list(ngrams(tokens, 3))
            for found in bigrams:
                full_ngrams_list.append(found)

            # get ngrams - 4
            bigrams = list(ngrams(tokens, 4))
            for found in bigrams:
                full_ngrams_list.append(found)

            # get ngrams - 5
            bigrams = list(ngrams(tokens, 5))
            for found in bigrams:
                full_ngrams_list.append(found)

            # get ngrams - 6
            bigrams = list(ngrams(tokens, 6))
            for found in bigrams:
                full_ngrams_list.append(found)

    total_counter = Counter(full_ngrams_list)
    counter_list = total_counter.most_common()
    for counter_element in counter_list:
        if counter_element[1] >= occurence_frequency:
            tuple = counter_element[0]
            bigram_tuples.append(tuple)
    return bigram_tuples

def create_word2vec_model():

    preprocessed_data = pd.read_excel(v.transformed_text_path_stage_4, sheet_name=v.input_file_sheet_name)
    selected_data = pd.DataFrame(preprocessed_data, columns=v.input_file_columns)
    selected_data['transformedtokens'] = selected_data['transformedtokens'].str.strip() # strip rows in series

    sentences = []
    sentence_list = list(selected_data['transformedtokens'])
    for sentence in sentence_list:
        sentences.append(sentence.split(' '))

    window_size = 3
    min_count = 5
    iteration_number = 3000
    vector_size = 200
    threads_number = 8
    #skim_gram = 1
    CBOW      = 0
    hierarchical_softmax = 1
    negatice_sampleing   = 0
    model = gensim.models.Word2Vec(
                        sentences
                        ,sg = CBOW
                        ,window=window_size
                        ,min_count= min_count
                        ,iter=iteration_number
                        ,size=vector_size
                        ,workers=threads_number
                        ,hs=hierarchical_softmax
                        ,negative = negatice_sampleing
                    )

    model.save('../data/fluid/input-output-word2vec-model')

def print_to_file(file_path, list, headings):
    data_frame = pd.DataFrame(list, columns=headings)
    data_frame.to_excel(file_path)

def get_proper_string(str):
    try:
        if math.isnan(str): return ' '
        return str
    except:
        return str
