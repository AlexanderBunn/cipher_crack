import os
import numpy
from pickle import load, dump
from tensorflow.keras import backend
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Input, Dense, Flatten, Dropout, Embedding, Conv1D, MaxPooling1D, concatenate

import tensorflow as tf
from tensorflow.python.util import deprecation

deprecation._PRINT_DECPRECATION_WARNINGS = False
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

CHAR_ENCODE = {
    ' ' : 1,
    'E' : 2,
    'T' : 3,
    'A' : 4,
    'O' : 5,
    'I' : 6,
    'N' : 7,
    'S' : 8,
    'R' : 9,
    'H' : 10,
    'D' : 11,
    'L' : 12,
    'U' : 13,
    'C' : 14,
    'M' : 15,
    'F' : 16,
    'Y' : 17,
    'W' : 18,
    'G' : 19,
    'P' : 20,
    'B' : 21,
    'V' : 22,
    'K' : 23,
    'X' : 24,
    'Q' : 25,
    'J' : 26,
    'Z' : 27
}

class NeuralNetwork():
    def __init__(self, ext):
        self.ext = ext
        self.model = self.load_model()
        self.tokenizer = self.load_tokenizer()
        self.embed_len = 27
        self.max_msg_len = 256
        self.ready()

    def ready(self):
        if self.model == None: # or self.tokenizer == None:
            print('Files missing, please rebuild.')
            return False
        return True

    def load_tokenizer(self):
        if os.path.isfile('./cache/t_' + self.ext + '.pkl'):
            return load(open('./cache/t_' + self.ext + '.pkl', 'rb'))
        return None

    def load_model(self):
        if os.path.isfile('./cache/m_' + self.ext + '.h5'):
            return load_model('./cache/m_' + self.ext + '.h5')
        return None

    # def rebuild_tokenizer(self, lines):
    #     self.tokenizer = Tokenizer(num_words=27)
    #     self.tokenizer.fit_on_texts(lines)
    #     tokens = len(self.tokenizer.word_index) + 1
    #     self.embed_len = tokens
    #     dump(self.tokenizer, open('./cache/t_' + self.ext + '.pkl', 'wb'))

    def rebuild_model(self):
        self.model = self.define_model()

    def vectorize(self, lines):
        # print(lines[0])
        # encoded1 = self.tokenizer.texts_to_sequences(lines)
        encoded2 = [[CHAR_ENCODE[c] for c in l] for l in lines]
        # charset = set()
        # for ll, el in zip(lines, encoded):
        #     for lc, ec in zip(ll, el):
        #         charset.add((lc, ec,))
        # print('LENGTH:', len(charset))
        # for chars in charset:
        #     print(chars)
        # input()
        # padded1 = pad_sequences(encoded1, maxlen=self.max_msg_len, padding='post')
        padded2 = pad_sequences(encoded2, maxlen=self.max_msg_len, padding='post')
        # print(padded[0])
        # print(padded1)
        # input(padded2)
        return padded2

    def train(self, lines, labels, batch_size):
        X, Y = self.inputs(lines, labels)
        self.model.fit(X, Y, epochs=1, batch_size=batch_size)

    def test(self, lines, labels):
        X, Y = self.inputs(lines, labels)
        loss, acc = self.model.evaluate(X, Y, verbose=0)

    def save(self):
        self.model.save('./cache/m_' + self.ext + '.h5')

    def run_model(self, lines):
        if not self.ready():
            return None
        X, Y = self.inputs(lines, [])
        preds = self.model.predict(X)
        return preds

class CNN(NeuralNetwork):

    def __init__(self, ext):
        super().__init__(ext)

    def inputs(self, lines, labels):
        X = self.vectorize(lines)
        # print(X)
        # input(labels)
        return [X, X, X, X, X], labels

    def define_model(self):
        # COPIED CODE
        # channel 1
        inputs1 = Input(shape=(self.max_msg_len,))
        embedding1 = Embedding(input_dim=self.embed_len, output_dim=self.max_msg_len, input_length=self.max_msg_len)(inputs1)
        conv1 = Conv1D(filters=32, kernel_size=2, activation='relu')(embedding1)
        drop1 = Dropout(0.5)(conv1)
        pool1 = MaxPooling1D(pool_size=2)(drop1)
        flat1 = Flatten()(pool1)
        # channel 2
        inputs2 = Input(shape=(self.max_msg_len,))
        embedding2 = Embedding(input_dim=self.embed_len, output_dim=self.max_msg_len, input_length=self.max_msg_len)(inputs2)
        conv2 = Conv1D(filters=32, kernel_size=3, activation='relu')(embedding2)
        drop2 = Dropout(0.5)(conv2)
        pool2 = MaxPooling1D(pool_size=2)(drop2)
        flat2 = Flatten()(pool2)
        # channel 3
        inputs3 = Input(shape=(self.max_msg_len,))
        embedding3 = Embedding(input_dim=self.embed_len, output_dim=self.max_msg_len, input_length=self.max_msg_len)(inputs3)
        conv3 = Conv1D(filters=32, kernel_size=4, activation='relu')(embedding3)
        drop3 = Dropout(0.5)(conv3)
        pool3 = MaxPooling1D(pool_size=2)(drop3)
        flat3 = Flatten()(pool3)
        # channel 4
        inputs4 = Input(shape=(self.max_msg_len,))
        embedding4 = Embedding(input_dim=self.embed_len, output_dim=self.max_msg_len, input_length=self.max_msg_len)(inputs4)
        conv4 = Conv1D(filters=32, kernel_size=5, activation='relu')(embedding4)
        drop4 = Dropout(0.5)(conv4)
        pool4 = MaxPooling1D(pool_size=2)(drop4)
        flat4 = Flatten()(pool4)
        # channel 5
        inputs5 = Input(shape=(self.max_msg_len,))
        embedding5 = Embedding(input_dim=self.embed_len, output_dim=self.max_msg_len, input_length=self.max_msg_len)(inputs5)
        conv5 = Conv1D(filters=32, kernel_size=6, activation='relu')(embedding5)
        drop5 = Dropout(0.5)(conv5)
        pool5 = MaxPooling1D(pool_size=2)(drop5)
        flat5 = Flatten()(pool5)
        # merge
        merged = concatenate([flat1, flat2, flat3, flat4, flat5])
        # interpretation
        dense1 = Dense(10, activation='relu')(merged)
        outputs = Dense(1)(dense1)
        model = Model(inputs=[inputs1, inputs2, inputs3, inputs4, inputs5], outputs=outputs)
        # compile
        model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        # summarize
        # print(model.summary())
        # plot_model(model, show_shapes=True, to_file='./multichannel.png')
        return model
