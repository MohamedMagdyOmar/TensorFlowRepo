# this code comes from below website with some modification
# https://machinelearningmastery.com/sequence-classification-lstm-recurrent-neural-networks-python-keras/

import numpy as np
import data_helper as dp
from keras.models import load_model
import SukunCorrection
import datetime
import FathaCorrection
import DictionaryCorrection
import DERCalculationHelperMethod
import WordLetterProcessingHelperMethod
import ExcelHelperMethod
from copy import deepcopy
import DBHelperMethod
import itertools
import os
import numpy
from time import sleep
from keras import backend as K
# fix random seed for reproducibility


class MasterObject:
    rnn_diac_char = "",
    rnn_diac = "",
    rnn_diac_word = "",
    undiac_char = "",
    location_in_word = "",
    location_in_sent = "",
    undiac_word = "",
    exp_diac_char = "",
    exp_diac = "",
    exp_diac_word = "",
    has_next_char = False,
    has_prev_char = False,
    sentence = ""
    value = 0

    def __init__(self):
        self.rnn_diac_char = ""
        self.rnn_diac = ""
        self.undiac_char = ""
        self.location_in_word = ""
        self.location_in_sent = ""
        self.undiac_word = ""
        self.exp_diac_char = ""
        self.exp_diac = ""
        self.has_next_char = False
        self.has_prev_char = False
        self.sentence = ""
        self.rnn_diac_word = ""
        self.exp_diac_word = ""
        self.value = 0


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
current_row_1 = 0
current_row_2 = 0
Total_Error = 0
Total_Error_without_last_char = 0
req_char_index = 6
window_size = 8
error = []
error_without_last_letter = []


def prepare_master_object(selected_sentence, rnn_op, exp_op, location, undiac_words):

    list_of_master_object = []
    list_of_word_len = []
    total_length = 0
    letter_counter = 0
    if len(rnn_op) != len(exp_op) != len(location):
        raise Exception("bug found in data")

    for each_word in undiac_words:
        if each_word != 'space':
            decomposed_word = WordLetterProcessingHelperMethod.decompose_word_into_letters(each_word)
            total_length += len(decomposed_word)
            list_of_word_len.append(total_length)

    master = MasterObject()
    for (each_rnn_char, each_exp_char, each_location) in (zip(rnn_op, exp_op, location)):
        if each_rnn_char == 'space':
            continue

        master.undiac_char = WordLetterProcessingHelperMethod.remove_diacritics_from_this(each_rnn_char)
        master.rnn_diac_char = each_rnn_char
        decomposed_result_1 = WordLetterProcessingHelperMethod.decompose_diac_char_into_char_and_diacritics\
            (each_rnn_char)

        if len(decomposed_result_1) == 1:
            master.rnn_diac = ''

        elif len(decomposed_result_1) == 2 and decomposed_result_1[1] != u'ْ':
            master.rnn_diac = decomposed_result_1[1]
        elif len(decomposed_result_1) == 2 and decomposed_result_1[1] == u'ْ':
            master.rnn_diac = ''
            master.rnn_diac_char = master.undiac_char
        elif len(decomposed_result_1) == 3:
            master.rnn_diac = decomposed_result_1[1] + decomposed_result_1[2]

        master.exp_diac_char = each_exp_char
        decomposed_result_2 = WordLetterProcessingHelperMethod.decompose_diac_char_into_char_and_diacritics\
            (each_exp_char)

        if len(decomposed_result_2) == 1:
            master.exp_diac = ''
        elif len(decomposed_result_2) == 2 and decomposed_result_2[1] != u'ْ':
            master.exp_diac = decomposed_result_2[1]
        elif len(decomposed_result_2) == 2 and decomposed_result_2[1] == u'ْ':
            master.exp_diac = ''
            master.exp_diac_char = master.undiac_char
        elif len(decomposed_result_2) == 3:
            master.exp_diac = decomposed_result_2[1] + decomposed_result_2[2]

        master.location_in_word = each_location
        master.location_in_sent = letter_counter
        master.sentence = selected_sentence

        index = 0
        for each_length_index in range(0, len(list_of_word_len)):
            index = each_length_index
            if list_of_word_len[each_length_index] >= (letter_counter + 1):
                break

        master.undiac_word = undiac_words[index]

        if each_location == 'first' and list_of_word_len[index] != 1:
            master.has_next_char = True
            master.has_prev_char = False

        elif each_location == 'first' and len(list(master.undiac_word)) == 1:
            master.has_next_char = False
            master.has_prev_char = False

        elif each_location == 'middle':
            master.has_next_char = True
            master.has_prev_char = True

        elif each_location == 'last':
            master.has_next_char = False
            master.has_prev_char = True

        list_of_master_object.append(deepcopy(master))
        letter_counter += 1

    list_of_rnn_words = WordLetterProcessingHelperMethod.reform_word_from_version_2(list_of_master_object)
    st_range = 0
    for each_number in list_of_word_len:
        en_range = each_number

        for index in range(st_range, en_range):
            list_of_master_object[index].rnn_diac_word = list_of_rnn_words[0]
            list_of_master_object[index].exp_diac_word = selected_sentence[0]
        del list_of_rnn_words[0]
        del selected_sentence[0]
        st_range = en_range

    return list_of_master_object


def load_testing_data():
    dp.establish_db_connection()
    testing_dataset = DBHelperMethod.load_dataset_by_type("testing")
    #testing_dataset = DBHelperMethod.load_dataset_by_type_and_sentence_number_for_testing_purpose("testing", 3062)

    x = dp.load_nn_input_dataset_string_space_only(testing_dataset[:, [0, 6]])
    y = dp.load_nn_labels_dataset_string(testing_dataset[:, [0, 1]])

    sent_num, sen_len = dp.load_nn_seq_lengths(testing_dataset[:, [3]])
    sentences_padded, vocabulary, vocabulary_inv = dp.pad_sentences1(x, sen_len, req_char_index, window_size)

    testing_words = np.take(testing_dataset, 4, axis=1)
    input_testing_letters = np.take(testing_dataset, 0, axis=1)
    op_testing_letters = np.take(testing_dataset, 5, axis=1)
    sent_num = np.take(testing_dataset, 3, axis=1)
    letters_loc = np.take(testing_dataset, 6, axis=1)
    undiac_word = np.take(testing_dataset, 7, axis=1)

    return sentences_padded, y, vocabulary, vocabulary_inv, testing_words, input_testing_letters, op_testing_letters,\
           sent_num, letters_loc, undiac_word


def get_all_undiac_words(word_type):
    return DBHelperMethod.get_all_un_diacritized_words_in_sentences(word_type)


def get_undiac_words_for_selected_sentence(list_of_all_words_and_sent_num, sentence_number):

    list_of_undiac_words_and_sent = list_of_all_words_and_sent_num[
        list(np.where(list_of_all_words_and_sent_num == str(sentence_number))[0])]

    return list_of_undiac_words_and_sent[:, 0].tolist()


def get_all_dic_words():
    return DBHelperMethod.get_dictionary()


def get_dic_words_for_selected_sentence(dic, undiac_words):

    dictionary = dic[:, 1]
    list_of_indices = []
    for each_word in undiac_words:
        list_of_indices.append([i for i, x in enumerate(dictionary) if x == each_word])

    indices = list(itertools.chain(*list_of_indices))
    return dic[indices]


def create_vocab():

    DBHelperMethod.connect_to_db()
    dataset = DBHelperMethod.load_data_set()
    chars = dp.load_nn_input_dataset_string(dataset[:, [0, 6]])
    vocab, vocab_inv = dp.build_vocab(chars)
    return vocab, vocab_inv, chars, dataset


if __name__ == "__main__":

    X_test, y_test, vocabulary_test, vocabulary_inv_test, words, ip_letters, op_letters, sentences_num, loc, \
    undiac_word = load_testing_data()
    dictionary = get_all_dic_words()

    model = load_model('weights.008-0.9344.hdf5')
    print(model.summary())
    prediction = model.predict(X_test, verbose=1)

    nn_indices = prediction.argmax(axis=1)
    expected_indices = y_test.argmax(axis=1)

    labels = dp.get_label_table()

    nn_labels = labels[nn_indices]
    nn_labels = np.take(nn_labels, 1, axis=1)
    expected_labels = labels[expected_indices]
    expected_labels = np.take(expected_labels, 1, axis=1)

    if len(nn_labels) == len(expected_labels) and len(nn_labels) == len(ip_letters):
        pass
    else:
        raise Exception("mismatch in number of elements in the array")

    nn_op_letters = dp.concatenate_char_and_diacritization(ip_letters, nn_labels)
    expected_op_letters = op_letters

    list_of_sentence_numbers = DBHelperMethod.get_list_of_sentence_numbers_by('testing')
    list_of_all_words_and_sent_num = get_all_undiac_words('testing')

    current_sentence_counter = 0
    counter = 0
    start_range = 0
    end_range = 0
    all_sentences = DBHelperMethod.get_all_sentences_by('testing')
    for sentence_number in list_of_sentence_numbers:
        #sentence_number = 3062
        print("we will begin processing in sentence number:", sentence_number)
        indices_of_selected_sentence = np.where(all_sentences == str(sentence_number))
        selected_sentence1 = list(all_sentences[indices_of_selected_sentence[0], 0])

        #selected_sentence1 = DBHelperMethod.get_sentence_by(sentence_number, 'testing')
        if len(selected_sentence1) == 0:
            start_range += 1
            continue

        undiac_words = get_undiac_words_for_selected_sentence(list_of_all_words_and_sent_num, sentence_number)

        dic_words_for_selected_sent = get_dic_words_for_selected_sentence(dictionary, undiac_words)

        num_of_chars_in_selected_sent = list(sentences_num).count(str(sentence_number))
        end_range = num_of_chars_in_selected_sent + start_range

        rnn_input = ip_letters[start_range: end_range: 1]

        nn_op_letters = dp.concatenate_char_and_diacritization(ip_letters[start_range: end_range: 1], nn_labels[start_range: end_range: 1])
        expected_letters = expected_op_letters[start_range: end_range: 1]
        location = loc[start_range: end_range: 1]

        master_object = prepare_master_object(deepcopy(selected_sentence1), nn_op_letters, expected_letters, location, undiac_words)

        # Post Processing
        RNN_Predicted_Chars_After_Fatha = FathaCorrection.fatha_correction_version_2(deepcopy(master_object))

        RNN_Predicted_Chars_After_Dictionary = DictionaryCorrection.\
            get_diac_version_with_smallest_dist_no_db_access_version_2\
            (RNN_Predicted_Chars_After_Fatha, dic_words_for_selected_sent)

        # DER Calculation
        start_time = datetime.datetime.now()
        error.append(DERCalculationHelperMethod.get_diacritization_error_version_2(RNN_Predicted_Chars_After_Dictionary,
                                                                                   sentence_number, selected_sentence1))

        error_without_last_letter.append(DERCalculationHelperMethod.
                                         get_diacritization_error_without_counting_last_letter_version_2
                                         (RNN_Predicted_Chars_After_Dictionary, sentence_number, selected_sentence1))
        '''
        Total_Error += len(error)
        print("Total Error: ", Total_Error)

        Total_Error_without_last_char += len(error_without_last_letter)
        print("Total Error without Last Char: ", Total_Error_without_last_char)
        '''
        counter += 1
        print("we are now in sentence # ", counter)

        start_range = end_range
        sleep(1)





error = list(itertools.chain.from_iterable(error))
error_without_last_letter = list(itertools.chain.from_iterable(error_without_last_letter))
ExcelHelperMethod.write_data_into_excel_file_version_2(error)
print("finished !!!")
K.clear_session()

