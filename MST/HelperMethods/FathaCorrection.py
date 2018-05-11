# -*- coding: utf-8 -*-

import unicodedata2
import WordLetterProcessingHelperMethod
import DERCalculationHelperMethod
letters_of_fatha_correction = [u'ة', u'ا', u'ى']


def fatha_correction(list_of_objects_of_chars_and_its_location):
    counter = 0
    current_index = 0
    actual_letters_after_fatha_correction = []

    prev_char_object = WordLetterProcessingHelperMethod.LetterPosition()
    prev_prev_char_object = WordLetterProcessingHelperMethod.LetterPosition()
    next_char_object = WordLetterProcessingHelperMethod.LetterPosition()

    for each_letter_object in list_of_objects_of_chars_and_its_location:

        actual_letters_after_fatha_correction.append(each_letter_object)
        character = remove_diacritics(each_letter_object.letter)

        if (character in letters_of_fatha_correction) and (each_letter_object.location != 'first'):

            letter_caused_fatha_correction = character

            if (counter - 1) >= 0:
                prev_char_object = list_of_objects_of_chars_and_its_location[counter - 1]
                prev_char_object.letter = unicodedata2.normalize('NFC', str(prev_char_object.letter))
            if (counter - 2) >= 0:
                prev_prev_char_object = list_of_objects_of_chars_and_its_location[counter - 2]
                prev_prev_char_object.letter = unicodedata2.normalize('NFC', prev_prev_char_object.letter)
            if ((counter + 1) <= (len(list_of_objects_of_chars_and_its_location) - 1)) and (each_letter_object.location != 'last'):
                next_char_object = list_of_objects_of_chars_and_its_location[counter + 1]

            corrected_char = prev_char_object.letter
            if letter_caused_fatha_correction == u'ة':
                corrected_char = correct_teh_marbota_prev_char(prev_char_object)

            elif letter_caused_fatha_correction == u'ا':

                if each_letter_object.location == 'middle':
                    if remove_diacritics(prev_char_object.letter) == u'ب':
                        # , بِاتِّخَاذِكُمُ ,وَبِالْآخِرَةِ , بِالْعُدْوَةِ
                        if u'ّ' in next_char_object.letter or\
                                        next_char_object.letter == remove_diacritics(next_char_object.letter):
                            corrected_char = correct_alef_prev_char_ba2_maksora(prev_char_object)

                        # بَالِغَةٌ , بَاسِرَةٌ
                        else:
                            corrected_char = correct_alef_prev_char_normal_case(prev_char_object)

                    elif remove_diacritics(prev_char_object.letter) == u'ل':
                        if prev_char_object.location == 'first':
                            # do not handle this case
                            # special case with no law (these are contradict) لَا , لِامْرَأَتِهِ
                            corrected_char = prev_char_object.letter

                        elif prev_prev_char_object.letter == u'ا':
                            # do not handle this case
                            # special case with no law (these are contradict)  الِاسْمُ
                            corrected_char = prev_char_object.letter
                        else:
                            corrected_char = correct_alef_prev_char_normal_case(prev_char_object)
                    # مِائَةَ , مِائَتَيْنِ
                    elif remove_diacritics(prev_char_object.letter) == u'م' \
                            and prev_char_object.location == 'first' \
                            and next_char_object.letter == u'ئَ':

                        corrected_char = correct_alef_prev_char_mem(prev_char_object)

                    else:
                        corrected_char = correct_alef_prev_char_normal_case(prev_char_object)

                elif each_letter_object.location == 'last' or each_letter_object.location == 'first':
                    corrected_char = prev_char_object.letter

                else:
                    corrected_char = correct_alef_prev_char_normal_case(prev_char_object)

            elif letter_caused_fatha_correction == u'ى':

                # طُوًى, ضُحًى
                if prev_prev_char_object.location == 'first' and u'ُ' in prev_prev_char_object.letter and \
                                each_letter_object.location == 'last':

                    corrected_char = correct_alef_maksora_prev_char_tanween_case(prev_char_object)

                # أَبَى
                else:
                    corrected_char = correct_alef_maksora_prev_char_normal_case(prev_char_object)

            actual_letters_after_fatha_correction[counter - 1].letter = corrected_char
            counter += 1
        else:
            counter += 1

        current_index += 1
    return actual_letters_after_fatha_correction


def fatha_correction(list_of_objects_of_chars_and_its_location, sentence):
    counter = 0
    current_index = 0
    actual_letters_after_fatha_correction = []

    prev_char_object = WordLetterProcessingHelperMethod.LetterPosition()
    prev_prev_char_object = WordLetterProcessingHelperMethod.LetterPosition()
    next_char_object = WordLetterProcessingHelperMethod.LetterPosition()

    for each_letter_object in list_of_objects_of_chars_and_its_location:

        actual_letters_after_fatha_correction.append(each_letter_object)
        character = remove_diacritics(each_letter_object.letter)

        if (character in letters_of_fatha_correction) and (each_letter_object.location != 'first'):

            letter_caused_fatha_correction = character

            if (counter - 1) >= 0:
                prev_char_object = list_of_objects_of_chars_and_its_location[counter - 1]
                prev_char_object.letter = unicodedata2.normalize('NFC', str(prev_char_object.letter))
            if (counter - 2) >= 0:
                prev_prev_char_object = list_of_objects_of_chars_and_its_location[counter - 2]
                prev_prev_char_object.letter = unicodedata2.normalize('NFC', prev_prev_char_object.letter)
            if ((counter + 1) <= (len(list_of_objects_of_chars_and_its_location) - 1)) and (each_letter_object.location != 'last'):
                next_char_object = list_of_objects_of_chars_and_its_location[counter + 1]

            corrected_char = prev_char_object.letter
            if letter_caused_fatha_correction == u'ة':
                corrected_char = correct_teh_marbota_prev_char(prev_char_object)

            elif letter_caused_fatha_correction == u'ا':

                if each_letter_object.location == 'middle':
                    if remove_diacritics(prev_char_object.letter) == u'ب':
                        # , بِاتِّخَاذِكُمُ ,وَبِالْآخِرَةِ , بِالْعُدْوَةِ
                        if u'ّ' in next_char_object.letter or\
                                        next_char_object.letter == remove_diacritics(next_char_object.letter):
                            corrected_char = correct_alef_prev_char_ba2_maksora(prev_char_object)

                        # بَالِغَةٌ , بَاسِرَةٌ
                        else:
                            corrected_char = correct_alef_prev_char_normal_case(prev_char_object)

                    elif remove_diacritics(prev_char_object.letter) == u'ل':
                        if prev_char_object.location == 'first':
                            # do not handle this case
                            # special case with no law (these are contradict) لَا , لِامْرَأَتِهِ
                            corrected_char = prev_char_object.letter

                        elif prev_prev_char_object.letter == u'ا':
                            # do not handle this case
                            # special case with no law (these are contradict)  الِاسْمُ
                            corrected_char = prev_char_object.letter
                        else:
                            corrected_char = correct_alef_prev_char_normal_case(prev_char_object)
                    # مِائَةَ , مِائَتَيْنِ
                    elif remove_diacritics(prev_char_object.letter) == u'م' \
                            and prev_char_object.location == 'first' \
                            and next_char_object.letter == u'ئَ':

                        corrected_char = correct_alef_prev_char_mem(prev_char_object)

                    else:
                        corrected_char = correct_alef_prev_char_normal_case(prev_char_object)

                elif each_letter_object.location == 'last' or each_letter_object.location == 'first':
                    corrected_char = prev_char_object.letter

                else:
                    corrected_char = correct_alef_prev_char_normal_case(prev_char_object)

            elif letter_caused_fatha_correction == u'ى':

                # طُوًى, ضُحًى
                if prev_prev_char_object.location == 'first' and u'ُ' in prev_prev_char_object.letter and \
                                each_letter_object.location == 'last':

                    corrected_char = correct_alef_maksora_prev_char_tanween_case(prev_char_object)

                # أَبَى
                else:
                    corrected_char = correct_alef_maksora_prev_char_normal_case(prev_char_object)

            actual_letters_after_fatha_correction[counter - 1].letter = corrected_char
            counter += 1
        else:
            counter += 1

        current_index += 1
    return actual_letters_after_fatha_correction


def fatha_correction_version_2(master_object):

    next_next_undiac_char = ''
    next_next_diac_char = ''

    for current_index in range(0, len(master_object)):

        current_undiac_char = master_object[current_index].undiac_char
        current_location = master_object[current_index].location_in_word
        if master_object[current_index].has_next_char:
            next_undiac_char = master_object[(current_index + 1)].undiac_char
            next_char_location = master_object[(current_index + 1)].location_in_word

            if master_object[(current_index + 1)].has_next_char:
                next_next_undiac_char = master_object[(current_index + 2)].undiac_char
                next_next_diac_char = master_object[(current_index + 2)].rnn_diac_char

            if next_undiac_char in letters_of_fatha_correction:

                if next_undiac_char == u'ة':
                    master_object[current_index].rnn_diac_char = \
                        teh_marbota_char_correction(master_object[current_index].rnn_diac_char)

                    master_object[current_index].rnn_diac = \
                        teh_marbota_char_correction(master_object[current_index].rnn_diac)

                elif next_undiac_char == u'ا':

                    if next_char_location == 'middle':
                        if current_undiac_char == u'ب':
                            # , بِاتِّخَاذِكُمُ ,وَبِالْآخِرَةِ , بِالْعُدْوَةِ
                            if u'ّ' in next_next_diac_char or next_next_diac_char == next_next_undiac_char:
                                master_object[current_index].rnn_diac_char = correct_alef_prev_char_ba2_maksora_version_2(master_object[current_index].rnn_diac_char)
                                master_object[current_index].rnn_diac = correct_alef_prev_char_ba2_maksora_version_2(master_object[current_index].rnn_diac)

                            # بَالِغَةٌ , بَاسِرَةٌ
                            else:
                                master_object[current_index].rnn_diac_char = correct_alef_prev_char_normal_case_version_2(master_object[current_index].rnn_diac_char)
                                master_object[current_index].rnn_diac = correct_alef_prev_char_normal_case_version_2(master_object[current_index].rnn_diac)

                        # مِائَةَ , مِائَتَيْنِ
                        elif current_undiac_char == u'م' \
                                and current_location == 'first' \
                                and next_next_diac_char == u'ئَ':
                            master_object[current_index].rnn_diac_char = correct_alef_prev_char_mem_version_2\
                                (master_object[current_index].rnn_diac_char)

                            master_object[current_index].rnn_diac = correct_alef_prev_char_mem_version_2 \
                                (master_object[current_index].rnn_diac)

                        else:
                            master_object[
                                current_index].rnn_diac_char = correct_alef_prev_char_normal_case_version_2(
                                master_object[
                                    current_index].rnn_diac_char)

                            master_object[
                                current_index].rnn_diac = correct_alef_prev_char_normal_case_version_2(master_object[
                                                                                                           current_index].rnn_diac)

                    else:
                        master_object[
                            current_index].rnn_diac_char = correct_alef_prev_char_normal_case_version_2(master_object[
                            current_index].rnn_diac_char)

                        master_object[
                            current_index].rnn_diac = correct_alef_prev_char_normal_case_version_2(master_object[
                            current_index].rnn_diac)

                elif next_undiac_char == u'ى':

                    if next_char_location == 'last' and master_object[current_index].rnn_diac != u'ً' and \
                            master_object[current_index].rnn_diac != u'َ':

                        master_object[
                            current_index].rnn_diac_char = correct_alef_maksora_prev_char_normal_case_version_2 \
                            (master_object[current_index].rnn_diac_char)

                        master_object[current_index].rnn_diac = correct_alef_maksora_prev_char_normal_case_version_2 \
                            (master_object[current_index].rnn_diac)

    return master_object


def fatha_correction_as_per_paper(master_object):
    next_next_undiac_char = ''
    next_next_diac_char = ''

    for current_index in range(0, len(master_object)):

        current_undiac_char = master_object[current_index].undiac_char
        current_location = master_object[current_index].location_in_word
        if master_object[current_index].has_next_char:
            next_undiac_char = master_object[(current_index + 1)].undiac_char
            next_char_location = master_object[(current_index + 1)].location_in_word

            if master_object[(current_index + 1)].has_next_char:
                next_next_undiac_char = master_object[(current_index + 2)].undiac_char
                next_next_diac_char = master_object[(current_index + 2)].rnn_diac_char

            if next_undiac_char in letters_of_fatha_correction:

                if next_undiac_char == u'ة':
                    master_object[current_index].rnn_diac_char = \
                        teh_marbota_char_correction(master_object[current_index].rnn_diac_char)

                    master_object[current_index].rnn_diac = \
                        teh_marbota_char_correction(master_object[current_index].rnn_diac)

                elif next_undiac_char == u'ا':

                    if next_char_location == 'middle':
                        if current_undiac_char == u'ب':
                            # , بِاتِّخَاذِكُمُ ,وَبِالْآخِرَةِ , بِالْعُدْوَةِ
                            if u'ّ' in next_next_diac_char or next_next_diac_char == next_next_undiac_char:
                                master_object[
                                    current_index].rnn_diac_char = correct_alef_prev_char_ba2_maksora_version_2(
                                    master_object[current_index].rnn_diac_char)
                                master_object[current_index].rnn_diac = correct_alef_prev_char_ba2_maksora_version_2(
                                    master_object[current_index].rnn_diac)

                            # بَالِغَةٌ , بَاسِرَةٌ
                            else:
                                master_object[
                                    current_index].rnn_diac_char = correct_alef_prev_char_normal_case_version_2(
                                    master_object[current_index].rnn_diac_char)
                                master_object[current_index].rnn_diac = correct_alef_prev_char_normal_case_version_2(
                                    master_object[current_index].rnn_diac)

                        # مِائَةَ , مِائَتَيْنِ
                        elif current_undiac_char == u'م' \
                                and current_location == 'first' \
                                and next_next_diac_char == u'ئَ':
                            master_object[current_index].rnn_diac_char = correct_alef_prev_char_mem_version_2 \
                                (master_object[current_index].rnn_diac_char)

                            master_object[current_index].rnn_diac = correct_alef_prev_char_mem_version_2 \
                                (master_object[current_index].rnn_diac)

                        else:
                            master_object[
                                current_index].rnn_diac_char = correct_alef_prev_char_normal_case_version_2(
                                master_object[
                                    current_index].rnn_diac_char)

                            master_object[
                                current_index].rnn_diac = correct_alef_prev_char_normal_case_version_2(master_object[
                                                                                                           current_index].rnn_diac)

                    else:
                        master_object[
                            current_index].rnn_diac_char = correct_alef_prev_char_normal_case_version_2(master_object[
                                                                                                            current_index].rnn_diac_char)

                        master_object[
                            current_index].rnn_diac = correct_alef_prev_char_normal_case_version_2(master_object[
                                                                                                       current_index].rnn_diac)

                elif next_undiac_char == u'ى':

                    if next_char_location == 'last' and master_object[current_index].rnn_diac != u'ً' and \
                            master_object[current_index].rnn_diac != u'َ':
                        master_object[
                            current_index].rnn_diac_char = correct_alef_maksora_prev_char_normal_case_version_2 \
                            (master_object[current_index].rnn_diac_char)

                        master_object[current_index].rnn_diac = correct_alef_maksora_prev_char_normal_case_version_2 \
                            (master_object[current_index].rnn_diac)

    return master_object


def remove_diacritics(character):
    nkfd_form = unicodedata2.normalize('NFKD', str(character))
    char = u"".join([c for c in nkfd_form if not unicodedata2.combining(c) or c == u'ٓ' or c == u'ٔ' or c == u'ٕ'])
    return char


def correct_teh_marbota_prev_char(prev_char):
    overall = ""
    comp = ""
    is_corrected = False
    for c in prev_char.letter:
        if not unicodedata2.combining(c):
            overall = c
            comp = unicodedata2.normalize('NFC', c)

        elif c == u'َ' or c == u'ّ' or c == u'ً':
            overall += c
            comp = unicodedata2.normalize('NFC', overall)
            is_corrected = True

        else:
            c = u'َ'
            overall += c
            comp = unicodedata2.normalize('NFC', overall)
            is_corrected = True

    if not is_corrected:
        c = u'َ'
        overall += c
        comp = unicodedata2.normalize('NFC', overall)

    return comp


def teh_marbota_char_correction(char):
    overall = ""
    comp = ""
    is_corrected = False
    for c in char:
        if not unicodedata2.combining(c):
            overall = c
            comp = unicodedata2.normalize('NFC', c)

        elif c == u'َ' or c == u'ّ' or c == u'ً':
            overall += c
            comp = unicodedata2.normalize('NFC', overall)
            is_corrected = True

        else:
            c = u'َ'
            overall += c
            comp = unicodedata2.normalize('NFC', overall)
            is_corrected = True

    if not is_corrected:
        c = u'َ'
        overall += c
        comp = unicodedata2.normalize('NFC', overall)

    return comp


def correct_alef_prev_char_ba2_maksora(prev_char_object):
    overall = ""
    comp = ""
    is_corrected = False
    for c in prev_char_object.letter:
        if not unicodedata2.combining(c):
            overall = c
            comp = unicodedata2.normalize('NFC', c)
        else:
            c = u'ِ'
            overall += c
            comp = unicodedata2.normalize('NFC', overall)
            is_corrected = True

    if not is_corrected:
        c = u'ِ'
        overall += c
        comp = unicodedata2.normalize('NFC', overall)

    return comp


def correct_alef_prev_char_ba2_maksora_version_2(letter):
    overall = ""
    comp = ""
    is_corrected = False
    for c in letter:
        if not unicodedata2.combining(c):
            overall = c
            comp = unicodedata2.normalize('NFC', c)
        else:
            c = u'ِ'
            overall += c
            comp = unicodedata2.normalize('NFC', overall)
            is_corrected = True

    if not is_corrected:
        c = u'ِ'
        overall += c
        comp = unicodedata2.normalize('NFC', overall)

    return comp


def correct_alef_prev_char_mem(prev_char_object):
    overall = ""
    comp = ""
    is_corrected = False
    for c in prev_char_object.letter:
        if not unicodedata2.combining(c):
            overall = c
            comp = unicodedata2.normalize('NFC', c)
        else:
            c = u'ِ'
            overall += c
            comp = unicodedata2.normalize('NFC', overall)
            is_corrected = True

    if not is_corrected:
        c = u'ِ'
        overall += c
        comp = unicodedata2.normalize('NFC', overall)
    return comp


def correct_alef_prev_char_mem_version_2(letter):
    overall = ""
    comp = ""
    is_corrected = False
    for c in letter:
        if not unicodedata2.combining(c):
            overall = c
            comp = unicodedata2.normalize('NFC', c)
        else:
            c = u'ِ'
            overall += c
            comp = unicodedata2.normalize('NFC', overall)
            is_corrected = True

    if not is_corrected:
        c = u'ِ'
        overall += c
        comp = unicodedata2.normalize('NFC', overall)
    return comp


def correct_alef_prev_char_normal_case(prev_char_object):
    overall = ""
    comp = ""
    is_corrected = False
    for c in prev_char_object.letter:
        if not unicodedata2.combining(c):
            overall = c
            comp = unicodedata2.normalize('NFC', c)

        elif c == u'َ' or c == u'ّ' or c == u'ً':
            overall += c
            comp = unicodedata2.normalize('NFC', overall)
            is_corrected = True

        else:
            c = u'َ'
            overall += c
            comp = unicodedata2.normalize('NFC', overall)
            is_corrected = True

    if not is_corrected:
        c = u'َ'
        overall += c
        comp = unicodedata2.normalize('NFC', overall)

    return comp


def correct_alef_prev_char_normal_case_version_2(letter):
    overall = ""
    comp = ""
    is_corrected = False
    for c in letter:
        if not unicodedata2.combining(c):
            overall = c
            comp = unicodedata2.normalize('NFC', c)

        elif c == u'َ' or c == u'ّ' or c == u'ً':
            overall += c
            comp = unicodedata2.normalize('NFC', overall)
            is_corrected = True

        else:
            c = u'َ'
            overall += c
            comp = unicodedata2.normalize('NFC', overall)
            is_corrected = True

    if not is_corrected:
        c = u'َ'
        overall += c
        comp = unicodedata2.normalize('NFC', overall)

    return comp


def correct_alef_maksora_prev_char_tanween_case(prev_char_object):
    overall = ""
    comp = ""
    is_corrected = False
    try:
        for c in prev_char_object.letter:
            if not unicodedata2.combining(c):
                overall = c
                comp = unicodedata2.normalize('NFC', c)

            elif c == u'َ' or c == u'ّ' or c == u'ً':
                overall += c
                comp = unicodedata2.normalize('NFC', overall)
                is_corrected = True

            else:
                c = u'ً'
                overall += c
                comp = unicodedata2.normalize('NFC', overall)
                is_corrected = True
    except:
        raise Exception("bug found in correct_alef_maksora_prev_char_tanween_case")

    if not is_corrected:
        c = u'ً'
        overall += c
        comp = unicodedata2.normalize('NFC', overall)

    return comp


def correct_alef_maksora_prev_char_tanween_case_version_2(letter):
    overall = ""
    comp = ""
    is_corrected = False
    try:
        for c in letter:
            if not unicodedata2.combining(c):
                overall = c
                comp = unicodedata2.normalize('NFC', c)

            elif c == u'َ' or c == u'ّ' or c == u'ً':
                overall += c
                comp = unicodedata2.normalize('NFC', overall)
                is_corrected = True

            else:
                c = u'ً'
                overall += c
                comp = unicodedata2.normalize('NFC', overall)
                is_corrected = True
    except:
        raise Exception("bug found in correct_alef_maksora_prev_char_tanween_case")

    if not is_corrected:
        c = u'ً'
        overall += c
        comp = unicodedata2.normalize('NFC', overall)

    return comp


def correct_alef_maksora_prev_char_normal_case(prev_char):
    overall = ""
    comp = ""
    is_corrected = False
    try:
        for c in prev_char.letter:
            if not unicodedata2.combining(c):
                overall = c
                comp = unicodedata2.normalize('NFC', c)

            elif c == u'َ' or c == u'ّ' or c == u'ً':
                overall += c
                comp = unicodedata2.normalize('NFC', overall)
                is_corrected = True

            else:
                c = u'َ'
                overall += c
                comp = unicodedata2.normalize('NFC', overall)
                is_corrected = True
    except:
        raise Exception("bug found in correct_alef_maksora_prev_char_normal_case")

    if not is_corrected:
        c = u'َ'
        overall += c
        comp = unicodedata2.normalize('NFC', overall)

    return comp


def correct_alef_maksora_prev_char_normal_case_version_2(letter):
    overall = ""
    comp = ""
    is_corrected = False
    try:
        for c in letter:
            if not unicodedata2.combining(c):
                overall = c
                comp = unicodedata2.normalize('NFC', c)

            elif c == u'َ' or c == u'ّ' or c == u'ً':
                overall += c
                comp = unicodedata2.normalize('NFC', overall)
                is_corrected = True

            else:
                c = u'َ'
                overall += c
                comp = unicodedata2.normalize('NFC', overall)
                is_corrected = True
    except:
        raise Exception("bug found in correct_alef_maksora_prev_char_normal_case")

    if not is_corrected:
        c = u'َ'
        overall += c
        comp = unicodedata2.normalize('NFC', overall)

    return comp