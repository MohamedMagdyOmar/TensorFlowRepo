from copy import deepcopy

import WordLetterProcessingHelperMethod
import DBHelperMethod
import SukunCorrection
import numpy as np
import itertools
from itertools import groupby


class OP_Req_Format:
    diac = '',
    letter = '',
    word = ''

    def __init__(self):
        self.diac = ""
        self.letter = ""
        self.word = ""


def get_diac_version_with_smallest_dist_no_db_access_version_2(master_object, dic_words):

    undiac_words = extract_correct_undiacritized_words_from_sentence(master_object)
    rnn_diac_words = extract_rnn_diacritized_word_of_this_sentence(undiac_words, master_object)

    selected_dictionary_word = ''
    selected_norm_dictionary_word = ''
    output = []

    for each_word, undiac_word in zip(rnn_diac_words, undiac_words):
        rows, cols = np.where(dic_words == undiac_word)

        dictionary_diacritized_words = (dic_words[rows, 0]).tolist()

        # no dictionary data found
        if len(dictionary_diacritized_words) == 0:
            output.append(extract_data_in_req_format(WordLetterProcessingHelperMethod.normalize \
                                                         (WordLetterProcessingHelperMethod.decompose_word_into_letters(
                                                             each_word)), each_word))

        else:
            dict_words_after_sukun_correction = SukunCorrection. \
                sukun_correction_for_list_of_words(dictionary_diacritized_words)

            minimum_error = 100000000
            for each_dic_word in dict_words_after_sukun_correction:
                error_count = 0

                norm_dic_word = WordLetterProcessingHelperMethod.normalize \
                        (WordLetterProcessingHelperMethod.decompose_word_into_letters(each_dic_word))

                norm_act_word = WordLetterProcessingHelperMethod.normalize \
                        (WordLetterProcessingHelperMethod.decompose_word_into_letters(each_word))

                # unify last char because it depend on context
                norm_dic_word[-1] = norm_act_word[-1]

                for each_dic_letter, each_act_letter in zip(norm_dic_word, norm_act_word):
                    if each_dic_letter[0] != each_act_letter[0] or each_dic_letter[1] != each_act_letter[1]:
                        error_count += 1

                if error_count < minimum_error:
                    minimum_error = error_count

                    selected_norm_dictionary_word = norm_dic_word
                    selected_dictionary_word = each_dic_word

            output.append(extract_data_in_req_format(selected_norm_dictionary_word, selected_dictionary_word))






    merged = list(itertools.chain(*output))
    if len(merged) != len(master_object):
        Exception("bug found")

    for index, (each_merged_object) in enumerate(merged):
        master_object[index].rnn_diac_char = each_merged_object.letter
        master_object[index].rnn_diac = each_merged_object.diac
        master_object[index].rnn_diac_word = each_merged_object.word

    return master_object


def extract_correct_undiacritized_words_from_sentence(master_object):

    undiac_words = []
    for each_word in master_object[0].sentence:
        undiac_words.append(WordLetterProcessingHelperMethod.remove_diacritics_from_this_word(each_word))

    return undiac_words


def extract_rnn_diacritized_word_of_this_sentence(undiac_words, master_object):
    rnn_diac_words = []
    for each_word in undiac_words:
        for each_object in master_object:
            if each_object.undiac_word == each_word:
                rnn_diac_words.append(each_object.rnn_diac_word)
                break

    return rnn_diac_words


def extract_data_in_req_format(norm_word, word):
    output = []

    for each_char in norm_word:
        word_format = OP_Req_Format()
        for each_item in reversed(each_char):
            word_format.letter += each_item

        if len(each_char) == 1:
            word_format.diac = ''
        elif len(each_char) == 2:
            word_format.diac = each_char[0]
        elif len(each_char) == 3:
            word_format.diac = each_char[0] + each_char[1]

        word_format.word = word
        output.append(deepcopy(word_format))

    return output