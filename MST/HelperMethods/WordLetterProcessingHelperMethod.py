# -*- coding: utf-8 -*-
import functools
import unicodedata
import locale
from copy import deepcopy


class LetterPosition:
    letter = "",
    location = "",
    value = ""

    def __init__(self):
        self.letter = ""
        self.location = ""
        self.value = ""


def get_location_of_each_char(list_of_chars, chars_count_for_each_word, remove_space):

    if remove_space:
        list_of_chars = list(filter(lambda a: a != 'space', list_of_chars))
        list_of_chars = list(filter(lambda a: a != 's', list_of_chars))

    list_of_chars_with_its_location = []
    i = 0

    sum = 0
    for each_number in chars_count_for_each_word:
        sum += each_number

    if sum != len(list_of_chars):
        raise ValueError('bug appeared in "get_location_of_each_character_in_current_sentence"')

    for count_of_letters in chars_count_for_each_word:
        letter_position_object = LetterPosition()
        for x in range(0, count_of_letters):
            if count_of_letters == 1:
                letter_position_object.letter = list_of_chars[i]
                letter_position_object.location = 'firstOneLetter'
                list_of_chars_with_its_location.append(deepcopy(letter_position_object))

            else:
                if x == 0:
                    letter_position_object.letter = list_of_chars[i]
                    letter_position_object.location = 'first'
                    list_of_chars_with_its_location.append(deepcopy(letter_position_object))

                elif x == (count_of_letters - 1):
                    letter_position_object.letter = list_of_chars[i]
                    letter_position_object.location = 'last'
                    list_of_chars_with_its_location.append(deepcopy(letter_position_object))

                else:
                    letter_position_object.letter = list_of_chars[i]
                    letter_position_object.location = 'middle'
                    list_of_chars_with_its_location.append(deepcopy(letter_position_object))

            i += 1

    return list_of_chars_with_its_location


def remove_diacritics_from_this_word(word):
    new_word = ''
    for each_char in word:
        nkfd_form = unicodedata.normalize('NFKD', str(each_char))
        char = u"".join([c for c in nkfd_form if not unicodedata.combining(c) or c == u'ٓ' or c == u'ٔ' or c == u'ٕ'])
        new_word += char
    return new_word


def remove_diacritics_from_this(character):
    nkfd_form = unicodedata.normalize('NFKD', str(character))
    char = u"".join([c for c in nkfd_form if not unicodedata.combining(c) or c == u'ٓ' or c == u'ٔ' or c == u'ٕ'])
    return char


def remove_diacritics_from(list_of_char_objects):
    undiacr_chars = []
    for each_object in list_of_char_objects:
        nkfd_form = unicodedata.normalize('NFKD', str(each_object.letter))
        each_object.letter = u"".join([c for c in nkfd_form if not unicodedata.combining(c) or c == u'ٓ' or c == u'ٔ' or c == u'ٕ'])
        undiacr_chars.append(each_object)
    return undiacr_chars


def reform_word_from(list_of_objects_of_chars_and_its_location):
    list_of_words = []
    word = ""
    isPrevWasLast = False
    for each_char_object in list_of_objects_of_chars_and_its_location:
        if each_char_object.location == 'firstOneLetter':
            list_of_words.append(each_char_object.letter)

        elif each_char_object.location != 'last':
            word += each_char_object.letter
            isPrevWasLast = False

        elif isPrevWasLast and each_char_object.location == 'last':
            word = each_char_object.letter
            list_of_words.append(word)
            isPrevWasLast = True
            word = ""

        elif each_char_object.location == 'last':
            word += each_char_object.letter
            list_of_words.append(word)
            isPrevWasLast = True
            word = ""

    return list_of_words


def reform_word_from_version_2(master):
    list_of_words = []
    word = ""
    isPrevWasLast = False
    for each_char_object in master:
        if each_char_object.location_in_word == 'firstOneLetter':
            list_of_words.append(each_char_object.rnn_diac_char)

        elif each_char_object.location_in_word != 'last':
            word += each_char_object.rnn_diac_char
            isPrevWasLast = False

        elif isPrevWasLast and each_char_object.location_in_word == 'last':
            word = each_char_object.rnn_diac_char
            list_of_words.append(word)
            isPrevWasLast = True
            word = ""

        elif each_char_object.location_in_word == 'last':
            word += each_char_object.rnn_diac_char
            list_of_words.append(word)
            isPrevWasLast = True
            word = ""

    return list_of_words


def decompose_word_into_letters(word):
    decomposed_word = []
    inter_med_list = []
    found_flag = False
    prev_letter = ''
    prev_symbol = 'kjshfkjshdfjhsdkjfhksdhkfhsalflasjdflkasdlkfsalkdjf'
    hamza_flag = False
    inter_med_list = ['', '', '']
    counter = 0
    for each_letter in word:

        if not unicodedata.combining(each_letter):
            prev_letter = each_letter
            counter = 0
            if prev_symbol == 'ٔ' or prev_symbol == 'ٕ' or prev_symbol == '':
                pass
            if found_flag:
                decomposed_word.append(inter_med_list)
                inter_med_list = ['', '', '']
            #inter_med_list.append(each_letter)
            inter_med_list[0] = each_letter
            counter += 1
            found_flag = True

        elif found_flag and each_letter != 'ٔ' and each_letter != 'ٕ':
            #inter_med_list.append(each_letter)
            if counter < 3:
                inter_med_list[counter] = each_letter
            counter += 1

        elif each_letter == 'ٔ' or each_letter == 'ٕ':
            hamza_flag = True
            each_letter = prev_letter + each_letter
            #inter_med_list.pop()
            #inter_med_list.append(each_letter)
            inter_med_list[0] = each_letter
            counter += 1

        if hamza_flag:
            hamza_flag = False
            prev_symbol = 'ٔ'

        else:
            prev_symbol = each_letter
    # required because last character will not be added above, but here
    decomposed_word.append(inter_med_list)

    return decomposed_word


def decompose_diac_char_into_char_and_diacritics(diac_char):
    decomposed_char = []

    for each_letter in diac_char:
        decomposed_char.append(each_letter)

    return decomposed_char


def normalize(word):
    locale.setlocale(locale.LC_ALL, "")
    for x in range(0, len(word)):
        word[x].sort(key=locale.strxfrm)

    return word


def convert_list_of_words_to_list_of_chars(list_of_words):
    found_flag = False
    overall = ""
    comp = ""
    final_list_of_actual_letters = []
    for each_word in list_of_words:
        for each_letter in each_word:
            x = unicodedata.combining(each_letter)
            if not unicodedata.combining(each_letter):
                if found_flag and comp != u'﻿':
                    final_list_of_actual_letters.append(comp)

                overall = each_letter
                found_flag = True
                comp = unicodedata.normalize('NFC', overall)
            elif found_flag:
                overall += each_letter
                comp = unicodedata.normalize('NFC', overall)

    final_list_of_actual_letters.append(comp)

    return final_list_of_actual_letters


def convert_list_of_words_to_list_of_chars_version2(master_object):
    found_flag = False
    overall = ""
    comp = ""
    final_list_of_actual_letters = []
    for each_object in master_object:
        for each_letter in each_object.rnn_diac_word:
            x = unicodedata.combining(each_letter)
            if not unicodedata.combining(each_letter):
                if found_flag and comp != u'﻿':
                    final_list_of_actual_letters.append(comp)

                overall = each_letter
                found_flag = True
                comp = unicodedata.normalize('NFC', overall)
            elif found_flag:
                overall += each_letter
                comp = unicodedata.normalize('NFC', overall)

    final_list_of_actual_letters.append(comp)

    return final_list_of_actual_letters


def attach_diacritics_to_chars(un_diacritized_chars, diacritics):
    list_chars_attached_with_diacritics = []

    if len(un_diacritized_chars) != len(diacritics):
        raise Exception('attach_diacritics_to_chars')

    for each_char, each_diacritics in zip(un_diacritized_chars, diacritics):
        list_chars_attached_with_diacritics.append((each_char + each_diacritics))

    return list_chars_attached_with_diacritics


def get_chars_count_for_each_word_in_this(sentence):
    count = 0
    chars_count_of_each_word = []
    for each_word in sentence:
        for each_char in each_word:
            if not unicodedata.combining(each_char) and each_char != u'﻿':
                count += 1
        chars_count_of_each_word.append(count)

        count = 0

    return chars_count_of_each_word


def check_target_and_output_letters_are_same(op, target):
    if len(op) != len(target):
        raise Exception("Bug Appeared In check_target_and_output_letters_are_same")
    required_list = []
    for x in range(0, len(op)):
        target_character = target[x][0]
        for diacritics_index in range(1, len(op[x])):
            target_character += op[x][diacritics_index]
        required_list.append(target_character)

    return required_list


def clean_data_from_shadda_only(list_of_words):
    for each_word in list_of_words:
        if each_word[0] == u'الصّالِحِيّ' or each_word[0] == u'السَّامَرَّائِيّ' or each_word[0] == u'التَّشِيلِيانِيّ':
            x = 1
        if each_word[0] != 'bos' and each_word[0] != 'eos' and each_word[0] != 'space':
            if u'\u0651' in each_word[0]:
                if each_word[0].count(u'\u0651') == 1:

                    if u'\u0651\u064e' in each_word[0] or u'\u0651\u064f' in each_word[0] \
                            or u'\u0651\u0650' in each_word[0] or u'\u0651\u064b' in each_word[0] \
                            or u'\u0651\u064c' in each_word[0] or u'\u0651\u064d' in each_word[0]:
                        x = 'do nothing'
                    else:
                        each_word[0] = each_word[0].replace(u'\u0651', u'\u0651\u064e')

                else:
                    length_of_array = len(each_word[0])
                    x = 0
                    while x < length_of_array:
                    # for x in range(0, length_of_array):
                        if each_word[0][x] == u'\u0651':
                            v = len(each_word[0])
                            if (x + 1) < len(each_word[0]):
                                try:
                                    if each_word[0][(x + 1)] != u'\u064e' and \
                                                each_word[0][(x + 1)] != u'\u064f' and \
                                                each_word[0][(x + 1)] != u'\u0650' and \
                                                each_word[0][(x + 1)] != u'\u064b' and \
                                                each_word[0][(x + 1)] != u'\u064c' and \
                                                each_word[0][(x + 1)] != u'\u064d' and \
                                                each_word[0][(x + 1)] != u'\u064e':

                                        b = list(each_word[0])
                                        b[x] = u'\u0651\u064e'
                                        each_word[0] = "".join(b)
                                        length_of_array += 1
                                        #each_word[0] = each_word[0].replace(each_word[0][x], u'\u0651\u064e')
                                        v = 1
                                except:
                                    x = 1

                            else:
                                b = list(each_word[0])
                                b[x] = u'\u0651\u064e'
                                each_word[0] = "".join(b)
                                length_of_array += 1
                                v = 1
                        x += 1


def append_neuron_op_value(actual_list, neuron_op_value):
    for each_object, each_neuron_value in zip(actual_list, neuron_op_value):
        each_object.value = each_neuron_value


def append_diacritics_with_un_diacritized_char(rnn_op, rnn_input, available_neuron_input):
    if len(rnn_op) != len(rnn_input):
        raise Exception("error appeared in append_diacritics_with_un_diacritized_char")

    letters = available_neuron_input[0:36]
    for each_op, each_input in zip(rnn_op, rnn_input):
        if each_op.letter != each_input:
            if each_op.letter in letters and each_input in letters:
                each_op.letter = each_input
            else:
                diac_char = each_input + each_op.letter
                each_op.letter = diac_char