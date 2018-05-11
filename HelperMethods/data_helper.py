import MySQLdb
import MySQLdb.cursors
import numpy as np
import datetime
import matplotlib
from collections import Counter
from itertools import chain
import unicodedata2


class LetterPosition:
    letter = "",
    location = "",
    value = ""

    def __init__(self):
        self.letter = ""
        self.location = ""
        self.value = ""


def establish_db_connection():
    db = MySQLdb.connect(host="127.0.0.1",  # your host, usually localhost
                         user="root",  # your username
                         passwd="Islammega88",  # your password
                         db="mstdb",  # name of the data base
                         cursorclass=MySQLdb.cursors.SSCursor,
                         use_unicode=True,
                         charset="utf8",
                         init_command='SET NAMES UTF8')
    global cur
    cur = db.cursor()

'''
def load_data_set():
    start_time = datetime.datetime.now()

    query = "select UnDiacritizedCharacter, Diacritics, LetterType, SentenceNumber,Word, DiacritizedCharacter, " \
            "location from ParsedDocument order by SentenceNumber asc"

    cur.execute(query)

    data = cur.fetchall()
    data = np.array(data)

    end_time = datetime.datetime.now()
    print("load_data_set takes : ", end_time - start_time)

    cur.close()
    return data

'''
'''
def load_dataset_by_type(data_type):

    start_time = datetime.datetime.now()
    establish_db_connection()
    query = "select UnDiacritizedCharacter, Diacritics, LetterType, SentenceNumber,Word, DiacritizedCharacter, " \
            "location, UnDiacritizedWord from ParsedDocument where LetterType=" + \
            "'%s'" % data_type + " order by SentenceNumber asc"

    cur.execute(query)

    data = cur.fetchall()
    data = np.array(data)

    end_time = datetime.datetime.now()
    print("load_dataset_by_type takes : ", end_time - start_time)
    cur.close()
    return data

'''
'''
def load_testing_dataset():

    start_time = datetime.datetime.now()
    establish_db_connection()
    query = "select UnDiacritizedCharacter, Diacritics, LetterType, SentenceNumber,Word, DiacritizedCharacter, " \
            "location, UnDiacritizedWord from ParsedDocument where LetterType=" + \
            "'%s'" % "testing"

    cur.execute(query)

    data = cur.fetchall()
    data = np.array(data)

    end_time = datetime.datetime.now()
    print("load_testing_dataset takes : ", end_time - start_time)
    cur.close()
    return data

'''


def load_cnn_blstm_table(data_type):
    start_time = datetime.datetime.now()

    query = "select UnDiacritizedCharacter, Diacritics, SentenceNumber, location from ParsedDocument where LetterType="\
            + "'%s'" % data_type

    cur.execute(query)

    data = cur.fetchall()
    data = np.array(data)

    end_time = datetime.datetime.now()
    print("load_cnn_blstm_table takes : ", end_time - start_time)

    return data


def get_input_table():
    start_time = datetime.datetime.now()
    establish_db_connection()
    query = "select UnDiacritizedCharacter, UnDiacritizedCharacterOneHotEncoding from UnDiacOneHotEncoding"
    cur.execute(query)

    input_and_equiv_encoding = cur.fetchall()
    input_and_equiv_encoding = np.array(input_and_equiv_encoding)

    end_time = datetime.datetime.now()
    print("get_db_input_table takes : ", end_time - start_time)
    cur.close()
    return input_and_equiv_encoding


def get_label_table():
    start_time = datetime.datetime.now()
    establish_db_connection()
    query = "select * from diacritics_and_undiacritized_letter_one_hot_encoding"
    cur.execute(query)

    labels_and_equiv_encoding = cur.fetchall()
    labels_and_equiv_encoding = np.array(labels_and_equiv_encoding)

    end_time = datetime.datetime.now()
    print("get_db_label_table takes : ", end_time - start_time)
    cur.close()
    return labels_and_equiv_encoding


def get_label_table_2():
    start_time = datetime.datetime.now()
    establish_db_connection()
    query = "select * from diaconehotencoding"
    cur.execute(query)

    labels_and_equiv_encoding = cur.fetchall()
    labels_and_equiv_encoding = np.array(labels_and_equiv_encoding)

    end_time = datetime.datetime.now()
    print("get_db_label_table takes : ", end_time - start_time)
    cur.close()
    return labels_and_equiv_encoding


def get_label_table_diacritics_only():
    start_time = datetime.datetime.now()
    establish_db_connection()
    query = "select * from distinctdiacritics"
    cur.execute(query)

    labels_and_equiv_encoding = cur.fetchall()
    labels_and_equiv_encoding = np.array(labels_and_equiv_encoding)

    end_time = datetime.datetime.now()
    print("get_db_label_table takes : ", end_time - start_time)
    cur.close()
    return labels_and_equiv_encoding


def load_nn_input_dataset_numpy(data_table):
    start_time = datetime.datetime.now()
    nn_input = []

    input_and_equiv_encoding = get_input_table()

    for each_row in data_table:
        raw_input_data = each_row[0]
        location = each_row[1]

        index_of_raw_input_data = np.where(input_and_equiv_encoding == raw_input_data)

        if np.size(index_of_raw_input_data) != 0:
            one_hot_encoding = input_and_equiv_encoding[np.min(index_of_raw_input_data[0]), 1]

            if location == 'first':
                one_hot_encoding = one_hot_encoding + '100'
            elif location == 'middle':
                one_hot_encoding = one_hot_encoding + '010'
            else:
                one_hot_encoding = one_hot_encoding + '001'

            nn_input.append(list(map(int, one_hot_encoding)))

    nn_input_np_array = np.array(nn_input)

    nn_input_np_array = nn_input_np_array.astype(np.float)

    end_time = datetime.datetime.now()

    print("load_nn_input_dataset_numpy takes : ", end_time - start_time)

    return nn_input_np_array


def load_nn_input_dataset_string(data_table):
    start_time = datetime.datetime.now()
    nn_input = []

    input_and_equiv_encoding = get_input_table()

    for each_row in data_table:
        raw_input_data = each_row[0]
        location = each_row[1]

        index_of_raw_input_data = np.where(input_and_equiv_encoding == raw_input_data)

        if np.size(index_of_raw_input_data) != 0:
            one_hot_encoding = input_and_equiv_encoding[np.min(index_of_raw_input_data[0]), 1]

            if location == 'first':
                one_hot_encoding = one_hot_encoding + '100'
            elif location == 'middle':
                one_hot_encoding = one_hot_encoding + '010'
            else:
                one_hot_encoding = one_hot_encoding + '001'

            nn_input.append(one_hot_encoding)

    end_time = datetime.datetime.now()

    print("load_nn_input_dataset_string takes : ", end_time - start_time)

    return np.array(nn_input)


def load_nn_input_dataset_string_space_only(data_table):
    start_time = datetime.datetime.now()
    nn_input = []

    input_and_equiv_encoding = get_input_table()

    for each_row in data_table:
        raw_input_data = each_row[0]

        index_of_raw_input_data = np.where(input_and_equiv_encoding == raw_input_data)

        if np.size(index_of_raw_input_data) != 0:
            one_hot_encoding = input_and_equiv_encoding[np.min(index_of_raw_input_data[0]), 1]

            nn_input.append(one_hot_encoding)
        else:
            Exception("Bug Found Here")

    end_time = datetime.datetime.now()

    print("load_nn_input_dataset_string takes : ", end_time - start_time)

    return np.array(nn_input)


def load_nn_input_dataset_one_to_one(data_table):
    start_time = datetime.datetime.now()
    nn_input = []

    inputs_and_equiv_encoding = get_input_table()

    for each_row in data_table:
        raw_input_data = each_row[0]

        index_of_raw_label_data = np.where(inputs_and_equiv_encoding == raw_input_data)

        if np.size(index_of_raw_label_data) != 0:
            input = inputs_and_equiv_encoding[index_of_raw_label_data[0], 1][0]
            input = input.replace('\n', "")
            input = list(map(int, input))

            nn_input.append(input)

    end_time = datetime.datetime.now()

    print("load_nn_input_dataset_one_to_one takes : ", end_time - start_time)

    return np.array(nn_input)


def load_nn_labels_dataset_numpy(data_table):
    start_time = datetime.datetime.now()
    nn_labels = []

    labels_and_equiv_encoding = get_label_table()

    for each_row in data_table:
        if each_row[1] != '':
            raw_input_data = each_row[1]
        else:
            raw_input_data = each_row[0]

        index_of_raw_label_data = np.where(labels_and_equiv_encoding == raw_input_data)

        if np.size(index_of_raw_label_data) != 0:
            label = np.min(index_of_raw_label_data[0])
            nn_labels.append(label)

    nn_label_np_array = np.array(nn_labels)

    nn_label_np_array = nn_label_np_array.astype(np.float)

    end_time = datetime.datetime.now()

    print("load_nn_labels_dataset_numpy takes : ", end_time - start_time)

    return nn_label_np_array


def load_nn_labels_dataset_string(data_table):
    start_time = datetime.datetime.now()
    nn_labels = []

    labels_and_equiv_encoding = get_label_table()
    labels_and_equiv_encoding = labels_and_equiv_encoding[:, [1, 2]]
    for each_row in data_table:
        if each_row[1] != '':
            raw_input_data = each_row[1]
        else:
            raw_input_data = each_row[0]

        index_of_raw_label_data = np.where(labels_and_equiv_encoding == raw_input_data)

        if np.size(index_of_raw_label_data) != 0:
            label = labels_and_equiv_encoding[index_of_raw_label_data[0], 1][0]
            label = label.replace('\n', "")
            label = list(map(int, label))

            nn_labels.append(label)
        else:
            Exception("Bug Here")

    end_time = datetime.datetime.now()

    print("load_nn_labels_dataset_string takes : ", end_time - start_time)

    return np.array(nn_labels)


def load_nn_labels_dataset_string_For_ATB(data_table):
    start_time = datetime.datetime.now()
    nn_labels = []

    labels_and_equiv_encoding = get_label_table()
    labels_and_equiv_encoding = labels_and_equiv_encoding[:, [1, 2]]
    for each_row in data_table:
        if each_row[1] != '':
            raw_input_data = each_row[1]
        else:
            raw_input_data = each_row[0]

        index_of_raw_label_data = np.where(labels_and_equiv_encoding == raw_input_data)

        if np.size(index_of_raw_label_data) != 0:
            label = labels_and_equiv_encoding[index_of_raw_label_data[0], 1][0]
            label = label.replace('\n', "")
            label = list(map(int, label))

            nn_labels.append(label)
        else:
            label = labels_and_equiv_encoding[50, 1]
            label = label.replace('\n', "")
            label = list(map(int, label))

            nn_labels.append(label)

    end_time = datetime.datetime.now()

    print("load_nn_labels_dataset_string takes : ", end_time - start_time)

    return np.array(nn_labels)


def load_nn_labels_dataset_string_2(data_table):
    start_time = datetime.datetime.now()
    nn_labels = []

    labels_and_equiv_encoding = get_label_table_2()

    for each_row in data_table:

        index_of_raw_label_data = np.where(labels_and_equiv_encoding == each_row[0])

        if np.size(index_of_raw_label_data) != 0:
            label = labels_and_equiv_encoding[index_of_raw_label_data[0], 2][0]
            label = label.replace('\n', "")
            label = list(map(int, label))

            nn_labels.append(label)
        else:
            Exception("bug here")

    end_time = datetime.datetime.now()

    print("load_nn_labels_dataset_string takes : ", end_time - start_time)

    return np.array(nn_labels)


def load_nn_labels_dataset_diacritics_only_string(data_table):
    start_time = datetime.datetime.now()
    nn_labels = []

    labels_and_equiv_encoding = get_label_table_diacritics_only()

    for each_row in data_table:

        raw_input_data = each_row[1]
        index_of_raw_label_data = np.where(labels_and_equiv_encoding == raw_input_data)

        if np.size(index_of_raw_label_data) != 0:
            label = labels_and_equiv_encoding[index_of_raw_label_data[0], 2][0]
            label = label.replace('\n', "")
            label = list(map(int, label))

            nn_labels.append(label)

    end_time = datetime.datetime.now()

    print("load_nn_labels_dataset_string takes : ", end_time - start_time)

    return np.array(nn_labels)


def load_nn_labels(data_table):
    start_time = datetime.datetime.now()
    labels = []
    for each_row in data_table:
        if each_row[1] != '':
            labels.append(each_row[1])
        else:
            labels.append(each_row[0])

    end_time = datetime.datetime.now()

    print("load_nn_labels_dataset_string takes : ", end_time - start_time)

    return np.array(labels)


def load_nn_seq_lengths(data_table):

    start_time = datetime.datetime.now()

    sent_num, sen_len = np.unique(np.hstack(data_table), return_counts=True)

    end_time = datetime.datetime.now()

    print("load_nn_seq_lengths takes : ", end_time - start_time)

    return sent_num, sen_len


def pad_sentences1(x, sent_len, req_char_index, window_size):
    start_time = datetime.datetime.now()

    padded_sent = []
    start_range = 0
    end_range = 0

    for each_sent in range(0, len(sent_len)):

        end_range = sent_len[each_sent] + end_range
        extracted_sent = x[start_range: end_range]
        padded_sent.append(padding1(extracted_sent, req_char_index, window_size))
        start_range = end_range

    end_time = datetime.datetime.now()

    vocabulary, vocabulary_inv = build_vocab(padded_sent)

    padded_sent = build_input_data(padded_sent, vocabulary)

    print("pad_sentences takes : ", end_time - start_time)

    return padded_sent, vocabulary, vocabulary_inv


def pad_sentences2(x, sent_len, req_char_index, window_size):
    start_time = datetime.datetime.now()

    padded_sent = []
    start_range = 0
    end_range = 0

    for each_sent in range(0, len(sent_len)):
        end_range = sent_len[each_sent] + end_range
        extracted_sent = x[start_range: end_range]
        padded_sent.append(padding1(extracted_sent, req_char_index, window_size))
        start_range = end_range

    end_time = datetime.datetime.now()
    print("pad_sentences takes : ", end_time - start_time)
    return padded_sent


def build_one_to_one_input_data(x, sent_len, req_char_index, window_size):
    start_time = datetime.datetime.now()

    vocabulary, vocabulary_inv = build_vocab(x)

    padded_sent = build_input_data_for_one_to_one(x, vocabulary)

    return padded_sent, vocabulary, vocabulary_inv
'''
def pad_sentences1(x, sent_len, window_size):
    start_time = datetime.datetime.now()

    padded_sent = []
    start_range = 0
    end_range = 0

    for each_sent in range(0, len(sent_len)):

        end_range = sent_len[each_sent] + end_range
        extracted_sent = x[start_range: end_range]
        padded_sent.append(padding1(extracted_sent, window_size))
        start_range = end_range

    end_time = datetime.datetime.now()

    vocabulary, vocabulary_inv = build_vocab(padded_sent)

    padded_sent = build_input_data(padded_sent, vocabulary)

    print("pad_sentences takes : ", end_time - start_time)

    return padded_sent, vocabulary, vocabulary_inv


def padding1(extracted_sent, req_char_index, window_size):

    padded_sent = []
    number_of_elements_before_target_char = req_char_index
    number_of_elements_after_target_char = window_size - req_char_index - 1
    for index in range(0, len(extracted_sent)):
        new_list = ['pad'] * window_size
        new_list[req_char_index - 1] = extracted_sent[index]

        # before req index
        end_range = index - 1
        start_range = index - number_of_elements_before_target_char
        #start_range = index - req_char_index
        if start_range < 0:
            start_range = 0

        if start_range >= 0 and end_range >= 0:
            extracted_chars_in_cert_range = extracted_sent[start_range: (end_range + 1)]
            num_of_elem = np.size(extracted_chars_in_cert_range)
            new_list[(req_char_index - num_of_elem): req_char_index] = extracted_chars_in_cert_range

        # after req index
        start_range = index + 1
        end_range = index + number_of_elements_after_target_char
        #end_range = index + req_char_index + 1
        if end_range >= np.size(extracted_sent):
            end_range = np.size(extracted_sent) - 1

        if start_range <= (np.size(extracted_sent) - 1) and end_range <= (np.size(extracted_sent) - 1):
            extracted_chars_in_cert_range = extracted_sent[start_range: (end_range + 1)]
            num_of_elem = np.size(extracted_chars_in_cert_range)
            new_list[(req_char_index + 1): (req_char_index + num_of_elem + 1)] = extracted_chars_in_cert_range

        padded_sent.append(new_list)

    return padded_sent
'''


def padding1(extracted_sent, req_char_index_non_zero_index, window_size):

    padded_sent = []
    extracted_chars_in_cert_range = ""
    number_of_elements_before_target_char = req_char_index_non_zero_index - 1
    number_of_elements_after_target_char = window_size - req_char_index_non_zero_index
    num_of_elem = 0
    for index in range(0, len(extracted_sent)):
        new_list = ['pad'] * window_size
        new_list[req_char_index_non_zero_index - 1] = extracted_sent[index]

        # before req index
        end_range_for_extracted_sent = index - 1
        start_range_for_extracted_sent = index - number_of_elements_before_target_char

        if start_range_for_extracted_sent < 0:
            start_range_for_extracted_sent = 0

        if end_range_for_extracted_sent >= 0 and number_of_elements_before_target_char > 0:
            extracted_chars_in_cert_range = extracted_sent[
                                            start_range_for_extracted_sent: (end_range_for_extracted_sent + 1)]
            num_of_elem = np.size(extracted_chars_in_cert_range)

        end_range_for_new_list = req_char_index_non_zero_index - 1
        start_range_for_new_list = end_range_for_new_list - num_of_elem
        if start_range_for_new_list < 0:
            start_range_for_new_list = 0

        if end_range_for_new_list > 0 and num_of_elem > 0 and number_of_elements_before_target_char > 0:
            new_list[start_range_for_new_list: (end_range_for_new_list)] = extracted_chars_in_cert_range

        # after req index
        start_range_for_extracted_sent = index + 1
        if start_range_for_extracted_sent == len(extracted_sent):
            number_of_elements_after_target_char = 0

        end_range_for_extracted_sent = index + number_of_elements_after_target_char

        if number_of_elements_after_target_char > 0 and end_range_for_extracted_sent >= len(extracted_sent):
            extracted_chars_in_cert_range = extracted_sent[
                                            start_range_for_extracted_sent:]
            num_of_elem = np.size(extracted_chars_in_cert_range)

        elif number_of_elements_after_target_char > 0:
            extracted_chars_in_cert_range = extracted_sent[
                                            start_range_for_extracted_sent: (end_range_for_extracted_sent + 1)]
            num_of_elem = np.size(extracted_chars_in_cert_range)

        start_range_for_new_list = req_char_index_non_zero_index
        end_range_for_new_list = start_range_for_new_list + num_of_elem
        if end_range_for_new_list > window_size:
            end_range_for_new_list = window_size - 1

        if num_of_elem > 0 and number_of_elements_after_target_char > 0 and end_range_for_new_list == window_size:
            new_list[start_range_for_new_list:] = extracted_chars_in_cert_range

        elif num_of_elem > 0 and number_of_elements_after_target_char > 0:
            new_list[start_range_for_new_list: end_range_for_new_list] = extracted_chars_in_cert_range

        padded_sent.append(new_list)

    return padded_sent


def extract_sent_and_pad(x, sent_len, T):
    start_time = datetime.datetime.now()

    padded_sent = []
    start_range = 0
    end_range = 0

    for each_sent in range(0, len(sent_len)):
        end_range = sent_len[each_sent] + end_range
        extracted_sent = x[start_range: end_range]
        after_padding = padding2(extracted_sent, T)
        for each_item in after_padding:
            padded_sent.append(each_item)
        start_range = end_range

    end_time = datetime.datetime.now()

    vocabulary, vocabulary_inv = build_vocab(padded_sent)

    padded_sent = build_input_data2(padded_sent, vocabulary)

    padded_sent = np.array(padded_sent)
    print("extract_sent_and_pad takes : ", end_time - start_time)

    return padded_sent, vocabulary, vocabulary_inv


def extract_sent_and_pad_output(y, sent_len, T):
    start_time = datetime.datetime.now()

    padded_sent = []
    start_range = 0
    end_range = 0
    pad_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    for each_sent in range(0, len(sent_len)):
        end_range = sent_len[each_sent] + end_range
        extracted_sent = y[start_range: end_range]
        extracted_sent = np.insert(extracted_sent, 49, values=0, axis=1)
        after_padding = padding2(extracted_sent, T)
        for each_seq in range(0, len(after_padding)):
            for each_chars in range(0, len(after_padding[each_seq])):
                if after_padding[each_seq][each_chars] == 'pad':
                    after_padding[each_seq][each_chars] = np.array(pad_array)

        for each_item in after_padding:
            padded_sent.append(each_item)

        start_range = end_range

    padded_sent = np.array(padded_sent)

    return padded_sent


def padding2(extracted_sent, T):
    padded_sent = []

    if len(extracted_sent) > T:
        division_result = int(len(extracted_sent) / T)
        reminder = len(extracted_sent) % T
        counter = 1
        for selected_window in range(0, (division_result * T), T):
            new_list = list(extracted_sent[selected_window: counter * T])
            padded_sent.append(new_list)
            counter += 1

        if reminder != 0:
            new_list = ['pad'] * T
            new_list[0: reminder] = extracted_sent[(len(extracted_sent) - reminder): len(extracted_sent)]
            padded_sent.append(list(new_list))

    elif len(extracted_sent) < T:
        new_list = ['pad'] * T
        new_list[0: len(extracted_sent)] = extracted_sent
        padded_sent.append(list(new_list))
    else:
        new_list = list(extracted_sent)
        padded_sent.append(new_list)

    return padded_sent


def build_vocab(sentences):
    start_time = datetime.datetime.now()
    all_chars = list(matplotlib.cbook.flatten(sentences))
    chars_counts = Counter(all_chars)

    # Mapping from index to char
    vocabulary_inv = [x[0] for x in chars_counts.most_common()]
    vocabulary_inv = list(sorted(vocabulary_inv))

    # Mapping from char to index
    vocabulary = {x: (i + 1) for i, x in enumerate(vocabulary_inv)}

    end_time = datetime.datetime.now()

    print("build_vocab takes : ", end_time - start_time)

    return [vocabulary, vocabulary_inv]


def build_input_data(sentences, vocabulary):
    sentences = list(chain(*sentences))
    x = np.array([[vocabulary[word] for word in sentence] for sentence in sentences])
    return x


def build_input_data_without_flattening(sentences, vocabulary):
    x = [[vocabulary[word] for word in sentence] for sentence in sentences]
    return x


def build_input_data_for_one_to_one(chars, vocabulary):

    x = [vocabulary[each_char] for each_char in chars]
    return x


def build_input_data2(sentences, vocabulary):
    x = ([[vocabulary[word] for word in sentence] for sentence in sentences])
    return x


def build_input_from_vocab(sentences, vocabulary):
    x = ([vocabulary[each_char] for each_char in sentences])
    return x


def create_letter_location_object(nn_labels, loc):
    list_of_chars_with_its_location = []
    for each_label, each_loc in zip(nn_labels, loc):
        letter_position_object = LetterPosition()

        letter_position_object.letter = each_label
        letter_position_object.location = each_loc

        list_of_chars_with_its_location.append(letter_position_object)

    return list_of_chars_with_its_location


def concatenate_char_and_diacritization(ip_letters, nn_labels):
    nn_diacritized_letters = []

    for ip_each_letter, each_nn_labels in zip(ip_letters, nn_labels):

        try:
            if each_nn_labels == 'space' or ip_each_letter == 'space':
                nn_diacritized_letters.append(ip_each_letter)
            elif each_nn_labels == 'pad' or ip_each_letter == 'pad':
                nn_diacritized_letters.append(ip_each_letter)
            else:

                if len(list(each_nn_labels)) > 1:
                    nn_diacritized_letters.append(ip_each_letter + each_nn_labels)

                elif each_nn_labels == '':
                    nn_diacritized_letters.append(ip_each_letter)

                elif not unicodedata2.combining(each_nn_labels):
                    nn_diacritized_letters.append(ip_each_letter)

                else:
                    nn_diacritized_letters.append(ip_each_letter + each_nn_labels)
        except:
            Exception("Bug Appeared Here")

    return nn_diacritized_letters


def create_3d_output_y_tensor(y, sent_len, T):

    padded_sent = []
    start_range = 0
    end_range = 0

    for each_sent in range(0, len(sent_len)):
        end_range = sent_len[each_sent] + end_range
        extracted_sent = y[start_range: end_range]
        after_padding = padding2(extracted_sent, T)
        for each_item in after_padding:
            padded_sent.append(each_item)
        start_range = end_range

    return padded_sent


if __name__ == "__main__":

    establish_db_connection()
    dataset = load_dataset_by_type('training')
    load_nn_input_dataset_numpy(dataset[:, [0, 8]])
    load_nn_labels_dataset_numpy(dataset[:, [0, 1]])
    load_nn_seq_lengths(dataset[:, [3]])
