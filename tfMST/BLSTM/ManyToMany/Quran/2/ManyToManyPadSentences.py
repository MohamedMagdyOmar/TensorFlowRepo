# this same as "test", but here you make a window of 5 chars, and if actual sentence is finished so you pad
# the sequence as per the github post explained, so this is considered as modification for "test" file

import numpy
import math
import data_helper as dp
import SequenceProcessing as sqp
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, Bidirectional
from keras.layers.embeddings import Embedding
from keras.layers import TimeDistributed
from keras.layers import Dropout
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
import DBHelperMethod
import os
from itertools import chain
# fix random seed for reproducibility

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

window_size = 6
sequence_length = window_size

pad_list = ['pad', 'pad', 'pad', 'pad', 'pad', 'pad', 'pad', 'pad']
pad_list_small = ['pad', 'pad']

'''
def pad_input_data(selected_sentence):

    all_sequences = []
    each_sequence = []
    counter = -1
    while len(selected_sentence) % window_size:
        selected_sentence = numpy.vstack((selected_sentence, numpy.array(pad_list)))

    for each_item in selected_sentence:
        counter += 1
        if each_item[1] != '':
            each_sequence.append(each_item[1])
        else:
            each_sequence.append(each_item[0])

        if counter == (window_size - 1):
            counter = -1
            all_sequences.append(numpy.array(each_sequence))
            each_sequence = []

    v = numpy.array(all_sequences)
    return numpy.array(all_sequences)


def pad_label_data(selected_sentence, one_hot_encoding):
    window_counter = -1
    nn_labels = []
    each_sequence = []
    while len(selected_sentence) % window_size:
        selected_sentence = numpy.vstack((selected_sentence, numpy.array(pad_list_small)))

    for each_row in selected_sentence:
        window_counter += 1
        if each_row[1] != '':
            raw_input_data = each_row[1]
        else:
            raw_input_data = each_row[0]

        index_of_raw_label_data = numpy.where(one_hot_encoding == raw_input_data)

        if numpy.size(index_of_raw_label_data) != 0:
            label = one_hot_encoding[index_of_raw_label_data[0], 2][0]
            label = list(map(int, label))
            each_sequence.append(label)

            if window_counter == (window_size - 1):
                window_counter = -1
                nn_labels.append(numpy.array(each_sequence))
                each_sequence = []
        else:
            Exception('label not found')

    return numpy.array(nn_labels)
'''


def pad_data(input, output, label_encoding):
    all_sequences = []
    each_sequence = []
    all_sequence_labels = []
    each_sequence_labels = []
    counter = -1

    while len(input) % window_size:
        input = numpy.vstack((input, numpy.array(pad_list)))
        output = numpy.vstack((output, numpy.array(pad_list_small)))

    for each_input_row, each_output_row in zip(input, output):
        counter += 1

        # for input

        each_sequence.append(each_input_row[0])

        # for output
        if each_output_row[1] != '':
            raw_input_data = each_output_row[1]
        else:
            raw_input_data = each_output_row[0]

        index_of_raw_label_data = numpy.where(label_encoding == raw_input_data)

        if numpy.size(index_of_raw_label_data) != 0:
            label = label_encoding[index_of_raw_label_data[0], 2][0]
            label = list(map(int, label))
            each_sequence_labels.append(label)
        else:
            Exception('label not found')

        if counter == (window_size - 1):
            counter = -1
            all_sequences.append(numpy.array(each_sequence))
            all_sequence_labels.append(numpy.array(each_sequence_labels))
            each_sequence = []
            each_sequence_labels = []

    return numpy.array(all_sequences), all_sequence_labels


def convert_input_to_vocab(input):
    sequence_list = numpy.array(input)
    vocabulary, vocabulary_inv = dp.build_vocab(sequence_list)
    sentences = list(chain(*sequence_list))

    padded_input = dp.build_input_data2(sentences, vocabulary)
    return numpy.array(padded_input), vocabulary, vocabulary_inv


def load_training_data():
    dp.establish_db_connection()
    sequence_list = []
    padded_output = []

    training_dataset = DBHelperMethod.load_dataset_by_type("training")
    sentence_numbers = DBHelperMethod.get_list_of_sentence_numbers_by("training")
    labels_and_equiv_encoding = dp.get_label_table()

    for each_sentence_number in sentence_numbers:
        selected_sentence = training_dataset[numpy.where(training_dataset[:, 3] == str(each_sentence_number))]
        x, y = pad_data(selected_sentence, selected_sentence[:, [0, 1]], labels_and_equiv_encoding)

        sequence_list.append(x)
        padded_output.append(y)

    padded_input, vocabulary, vocabulary_inv = convert_input_to_vocab(sequence_list)
    padded_output = numpy.array(list(chain(*padded_output)))

    return padded_input, padded_output, vocabulary, vocabulary_inv


def load_testing_data():
    dp.establish_db_connection()
    sequence_list = []
    padded_output = []

    training_dataset = DBHelperMethod.load_dataset_by_type("testing")
    sentence_numbers = DBHelperMethod.get_list_of_sentence_numbers_by("testing")
    labels_and_equiv_encoding = dp.get_label_table()

    for each_sentence_number in sentence_numbers:
        selected_sentence = training_dataset[numpy.where(training_dataset[:, 3] == str(each_sentence_number))]
        x, y = pad_data(selected_sentence, selected_sentence[:, [0, 1]], labels_and_equiv_encoding)

        sequence_list.append(x)
        padded_output.append(y)

    padded_input, vocabulary, vocabulary_inv = convert_input_to_vocab(sequence_list)
    padded_output = numpy.array(list(chain(*padded_output)))

    return padded_input, padded_output, vocabulary, vocabulary_inv


def check_key_exist(vocab_training, vocab_testing):

    if any(key in vocab_training for key in vocab_testing):
        pass
    else:
        raise Exception("keys are missing")


if __name__ == "__main__":

    X_train, y_train, vocabulary_train, vocabulary_inv_train = load_training_data()
    X_test, y_test, vocabulary_test, vocabulary_inv_test = load_testing_data()
    check_key_exist(vocabulary_train, vocabulary_test)

    # y_train = y_train.reshape(len(y_train), 5, 51)
    # y_test = y_test.reshape(len(y_test), 5, 51)

    # input dim
    vocabulary_size = len(vocabulary_inv_train)
    # output dim
    embedding_vector_length = 51

    model = Sequential()

    model.add(Embedding(vocabulary_size, embedding_vector_length, input_length=sequence_length))

    model.add(Bidirectional(LSTM(250, dropout=0.2, recurrent_dropout=0.2, return_sequences=True)))
    model.add(Bidirectional(LSTM(350, dropout=0.2, recurrent_dropout=0.2, return_sequences=True)))
    model.add(Bidirectional(LSTM(250, dropout=0.2, recurrent_dropout=0.2, return_sequences=True)))

    model.add(TimeDistributed(Dense(51, activation='softmax')))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())

    checkpoint = ModelCheckpoint('weights.{epoch:03d}-{val_acc:.4f}.hdf5', monitor='val_acc', verbose=1,
                                 save_best_only=True, mode='max')

    # check 5 epochs
    early_stop = EarlyStopping(monitor='val_acc', patience=5, mode='max')
    callbacks_list = [checkpoint, early_stop]

    model.fit(X_train, y_train, validation_data=(X_test, y_test),
              callbacks=callbacks_list, epochs=40, batch_size=64, verbose=1)

    # Final evaluation of the model
    scores = model.evaluate(X_test, y_test, verbose=0)
    print("Accuracy: %.2f%%" % (scores[1]*100))
