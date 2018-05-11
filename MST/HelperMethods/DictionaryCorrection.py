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


def get_diac_version_with_smallest_dist(list_of_objects, sentence_number):

    list_of_actual_words_after_dictionary_correction = []

    diacritized_rnn_op_words = WordLetterProcessingHelperMethod.reform_word_from(list_of_objects)
    undiacritized_words = DBHelperMethod.get_un_diacritized_words_from(sentence_number, 'testing')

    if len(diacritized_rnn_op_words) != len(diacritized_rnn_op_words):
        raise Exception("error appeared in get_diac_version_with_smallest_dist")

    for each_corrected_word, each_un_diacritized_word in zip(diacritized_rnn_op_words, undiacritized_words):

        minimum_error = 100000000
        dictionary_diacritized_words = DBHelperMethod.\
            get_dictionary_all_diacritized_version_of(each_un_diacritized_word)

        if len(dictionary_diacritized_words) == 0:
            dictionary_diacritized_words.append(each_corrected_word)

        dictionary_diacritized_words_after_sukun_correction = SukunCorrection.\
            sukun_correction_for_list_of_words(dictionary_diacritized_words)

        if do_we_need_to_search_in_dictionary(dictionary_diacritized_words_after_sukun_correction, each_corrected_word):

            for each_word in dictionary_diacritized_words_after_sukun_correction:
                error_count = 0

                decomposed_dic_word = WordLetterProcessingHelperMethod.decompose_word_into_letters(each_word)
                decomposed_act_word = WordLetterProcessingHelperMethod.decompose_word_into_letters(each_corrected_word)

                norm_dic_word = WordLetterProcessingHelperMethod.normalize(decomposed_dic_word)
                norm_act_word = WordLetterProcessingHelperMethod.normalize(decomposed_act_word)

                for each_diacritized_version_letter, each_current_word_letter in zip(norm_dic_word, norm_act_word):

                    if (len(each_diacritized_version_letter) - len(each_current_word_letter) == 1) or (
                            (len(each_diacritized_version_letter) - len(each_current_word_letter) == -1)):
                        error_count += 1

                    elif (len(each_diacritized_version_letter) - len(each_current_word_letter) == 2) or (
                            (len(each_diacritized_version_letter) - len(each_current_word_letter) == -2)):
                        error_count += 2

                    else:
                        for each_item_in_diacritized_version, each_item_in_current_word in \
                                zip(each_diacritized_version_letter, each_current_word_letter):
                            if each_item_in_diacritized_version != each_item_in_current_word:
                                error_count += 1

                if error_count < minimum_error:
                    minimum_error = error_count

                    selected_dictionary_word = each_word

            list_of_actual_words_after_dictionary_correction.append(selected_dictionary_word)
        else:
            list_of_actual_words_after_dictionary_correction.append(each_corrected_word)

    chars_after_dic_correction = WordLetterProcessingHelperMethod.convert_list_of_words_to_list_of_chars(list_of_actual_words_after_dictionary_correction)
    if len(list_of_objects) != len(chars_after_dic_correction):
        raise Exception("Error Happened Here")

    for x in range(0, len(list_of_objects)):
        list_of_objects[x].letter = chars_after_dic_correction[x]

    return list_of_objects


def get_diac_version_with_smallest_dist_no_db_access(list_of_objects, undiac_words, dic_words):

    list_of_objects = list(filter(lambda a: a.letter != 'spacespace', list_of_objects))
    list_of_objects = list(filter(lambda a: a.letter != 'space', list_of_objects))
    list_of_objects = list(filter(lambda a: a.letter != 's', list_of_objects))
    list_of_actual_words_after_dictionary_correction = []

    diacritized_rnn_op_words = WordLetterProcessingHelperMethod.reform_word_from(list_of_objects)
    undiacritized_words = undiac_words

    if len(diacritized_rnn_op_words) != len(undiacritized_words):
        raise Exception("error appeared in get_diac_version_with_smallest_dist")

    for each_corrected_word, each_un_diacritized_word in zip(diacritized_rnn_op_words, undiacritized_words):

        minimum_error = 100000000
        rows, cols = np.where(dic_words == each_un_diacritized_word)
        dictionary_diacritized_words = (dic_words[rows, 0]).tolist()

        if len(dictionary_diacritized_words) == 0:
            dictionary_diacritized_words.append(each_corrected_word)

        dictionary_diacritized_words_after_sukun_correction = SukunCorrection.\
            sukun_correction_for_list_of_words(dictionary_diacritized_words)

        if do_we_need_to_search_in_dictionary(dictionary_diacritized_words_after_sukun_correction, each_corrected_word):

            for each_word in dictionary_diacritized_words_after_sukun_correction:
                error_count = 0

                decomposed_dic_word = WordLetterProcessingHelperMethod.decompose_word_into_letters(each_word)
                decomposed_act_word = WordLetterProcessingHelperMethod.decompose_word_into_letters(each_corrected_word)

                norm_dic_word = WordLetterProcessingHelperMethod.normalize(decomposed_dic_word)
                norm_act_word = WordLetterProcessingHelperMethod.normalize(decomposed_act_word)

                for each_diacritized_version_letter, each_current_word_letter in zip(norm_dic_word, norm_act_word):

                    if (len(each_diacritized_version_letter) - len(each_current_word_letter) == 1) or (
                            (len(each_diacritized_version_letter) - len(each_current_word_letter) == -1)):
                        error_count += 1

                    elif (len(each_diacritized_version_letter) - len(each_current_word_letter) == 2) or (
                            (len(each_diacritized_version_letter) - len(each_current_word_letter) == -2)):
                        error_count += 2

                    else:
                        for each_item_in_diacritized_version, each_item_in_current_word in \
                                zip(each_diacritized_version_letter, each_current_word_letter):
                            if each_item_in_diacritized_version != each_item_in_current_word:
                                error_count += 1

                if error_count < minimum_error:
                    minimum_error = error_count

                    selected_dictionary_word = each_word

            list_of_actual_words_after_dictionary_correction.append(selected_dictionary_word)
        else:
            list_of_actual_words_after_dictionary_correction.append(each_corrected_word)

    chars_after_dic_correction = WordLetterProcessingHelperMethod.convert_list_of_words_to_list_of_chars(list_of_actual_words_after_dictionary_correction)
    if len(list_of_objects) != len(chars_after_dic_correction):
        raise Exception("Error Happened Here")

    for x in range(0, len(list_of_objects)):
        list_of_objects[x].letter = chars_after_dic_correction[x]

    return list_of_objects


def get_diac_version_with_smallest_dist_no_db_access_version_2(master_object, dic_words):

    # rnn_diac_words = [each_object.rnn_diac_word for each_object in master_object]
    # rnn_diac_words = [x[0] for x in groupby(rnn_diac_words1)]
    # rnn_diac_words = master_object[0].sentence
    undiac_words = []
    rnn_diac_words = []
    for each_word in master_object[0].sentence:
        undiac_words.append(WordLetterProcessingHelperMethod.remove_diacritics_from_this_word(each_word))

    for each_word in undiac_words:
        for each_object in master_object:
            if each_object.undiac_word == each_word:
                rnn_diac_words.append(each_object.rnn_diac_word)
                break

    #undiac_words = [each_object.undiac_word for each_object in master_object]
    #undiac_words = [x[0] for x in groupby(undiac_words)]

    selected_dictionary_word = ''
    selected_norm_dictionary_word = ''
    output = []
    for each_word, undiac_word in zip(rnn_diac_words, undiac_words):
        rows, cols = np.where(dic_words == undiac_word)

        dictionary_diacritized_words = []
        dictionary_diacritized_words = (dic_words[rows, 0]).tolist()

        # no dictionary data found
        if len(dictionary_diacritized_words) == 0:
            output.append(extract_data_in_req_format(WordLetterProcessingHelperMethod.normalize \
                                                         (WordLetterProcessingHelperMethod.decompose_word_into_letters(
                                                             each_word)), each_word))

        else:
            dict_words_after_sukun_correction = SukunCorrection. \
                sukun_correction_for_list_of_words(dictionary_diacritized_words)

            if not(do_we_need_to_search_in_dictionary(dict_words_after_sukun_correction, each_word)):
                output.append(extract_data_in_req_format(WordLetterProcessingHelperMethod.normalize \
                        (WordLetterProcessingHelperMethod.decompose_word_into_letters(each_word)), each_word))

            else:
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


def dictionary_correction_as_per_paper(master_object, dic_words):
    undiac_words = []
    rnn_diac_words = []
    for each_word in master_object[0].sentence:
        undiac_words.append(WordLetterProcessingHelperMethod.remove_diacritics_from_this_word(each_word))

    for each_word in undiac_words:
        for each_object in master_object:
            if each_object.undiac_word == each_word:
                rnn_diac_words.append(each_object.rnn_diac_word)
                break

    selected_dictionary_word = ''
    selected_norm_dictionary_word = ''
    output = []
    for each_word, undiac_word in zip(rnn_diac_words, undiac_words):
        rows, cols = np.where(dic_words == undiac_word)

        dictionary_diacritized_words = []
        dictionary_diacritized_words = (dic_words[rows, 0]).tolist()

        # no dictionary data found
        if len(dictionary_diacritized_words) == 0:
            output.append(extract_data_in_req_format(WordLetterProcessingHelperMethod.normalize \
                    (WordLetterProcessingHelperMethod.decompose_word_into_letters(
                    each_word)), each_word))

        else:
            dict_words_after_sukun_correction = SukunCorrection. \
                sukun_correction_for_list_of_words(dictionary_diacritized_words)

            if not(do_we_need_to_search_in_dictionary2(dict_words_after_sukun_correction, each_word)):
                output.append(extract_data_in_req_format(WordLetterProcessingHelperMethod.normalize \
                        (WordLetterProcessingHelperMethod.decompose_word_into_letters(each_word)), each_word))

            else:
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

def do_we_need_to_search_in_dictionary(dictionary, word):

    for each_word in dictionary:
        decomposed_dict = WordLetterProcessingHelperMethod.decompose_word_into_letters(each_word)
        decomposed_act = WordLetterProcessingHelperMethod.decompose_word_into_letters(word)

        norm_dict = WordLetterProcessingHelperMethod.normalize(decomposed_dict)
        norm_act = WordLetterProcessingHelperMethod.normalize(decomposed_act)

        if len(norm_dict) != len(norm_act):
            raise ValueError("Bug Found In 'do_we_need_to_search_in_dictionary'")

        if sorted(norm_dict) == sorted(norm_act):
            return False

    for each_word in dictionary:
        decomposed_dict = WordLetterProcessingHelperMethod.decompose_word_into_letters(each_word)
        decomposed_act = WordLetterProcessingHelperMethod.decompose_word_into_letters(word)

        norm_dict = WordLetterProcessingHelperMethod.normalize(decomposed_dict)
        norm_act = WordLetterProcessingHelperMethod.normalize(decomposed_act)

        for x in range(0, len(norm_act)):
            # compare letters before last letter
            if x < (len(norm_act) - 1):
                if norm_dict[x] != norm_act[x]:
                    # so diff is in first or middle letters
                    break
            else:
                # so diff is in last letter so ignore it
                return False

    return True


def do_we_need_to_search_in_dictionary2(dictionary, word):

    if word in dictionary:
        return False

    return True


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