# this code comes from below website with some modification
# https://machinelearningmastery.com/sequence-classification-lstm-recurrent-neural-networks-python-keras/

import numpy
import data_helper as dp
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, Bidirectional
from keras.layers.embeddings import Embedding
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
import DBHelperMethod
import os
# fix random seed for reproducibility
numpy.random.seed(7)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
req_char_index = 6
window_size = 8


def load_data():
    dp.establish_db_connection()

    training_dataset = DBHelperMethod.load_dataset_by_type("training")
    testing_dataset = DBHelperMethod.load_dataset_by_type("testing")

    x_training = dp.load_nn_input_dataset_string_space_only(training_dataset[:, [0, 6]])
    y_training = dp.load_nn_labels_dataset_string(training_dataset[:, [0, 1]])

    sent_num_training, sen_len_training = dp.load_nn_seq_lengths(training_dataset[:, [3]])
    sentences_padded_training = dp.pad_sentences2(x_training, sen_len_training, req_char_index, window_size)

    vocabulary, vocabulary_inv = dp.build_vocab(sentences_padded_training)
    padded_sent_training = dp.build_input_data(sentences_padded_training, vocabulary)

    x_testing = dp.load_nn_input_dataset_string_space_only(testing_dataset[:, [0, 6]])
    y_testing = dp.load_nn_labels_dataset_string(testing_dataset[:, [0, 1]])

    sent_num_testing, sen_len_testing = dp.load_nn_seq_lengths(testing_dataset[:, [3]])

    sentences_padded_testing = dp.pad_sentences2(x_testing, sen_len_testing, req_char_index, window_size)
    padded_sent_testing = dp.build_input_data(sentences_padded_testing, vocabulary)

    return padded_sent_training, y_training, vocabulary, vocabulary_inv, padded_sent_testing, y_testing



if __name__ == "__main__":

    X_train, y_train, vocabulary_train, vocabulary_inv_train, X_test, y_test = load_data()
    #X_train, y_train, vocabulary_train, vocabulary_inv_train = load_training_data()
    #X_test, y_test, vocabulary_test, vocabulary_inv_test = load_testing_data()
    # check_key_exist(vocabulary_train, vocabulary_test)

    sequence_length = 8
    max_review_length = sequence_length

    # input dim
    vocabulary_size = len(vocabulary_inv_train)
    # output dim
    embedding_vector_length = 220

    model = load_model('weights.004-0.9076.hdf5')

    # file_path = "weights.best.hdf5"
    checkpoint = ModelCheckpoint('weights.{epoch:03d}-{val_acc:.4f}.hdf5', monitor='val_acc', verbose=1,
                                 save_best_only=True, mode='max')

    # check 5 epochs
    early_stop = EarlyStopping(monitor='val_acc', patience=5, mode='max')
    callbacks_list = [checkpoint, early_stop]

    # Continue training
    model.fit(X_train, y_train, validation_data=(X_test, y_test),
              callbacks=callbacks_list, epochs=40, batch_size=64, verbose=1)
