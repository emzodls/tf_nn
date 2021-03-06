# Copyright (C) 2019 Emmanuel LC. de los Santos
# University of Warwick
# Warwick Integrative Synthetic Biology Centre
#
# License: GNU Affero General Public License v3 or later
# A copy of GNU AGPL v3 should have been included in this software package in LICENSE.txt.
'''
    This file is part of NeuRiPP.

    NeuRiPP is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    NeuRiPP is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with NeuRiPP.  If not, see <http://www.gnu.org/licenses/>.
'''

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential

def create_model_conv_parallel():
    input = keras.layers.Input(shape=(120, 20))
    kernel_sizes = [3,4,5]
    maps_per_kernel = 2
    convs = []
    for kernel_size in kernel_sizes:
        for map_n in range(maps_per_kernel):
            conv = keras.layers.Conv1D(filters=50,
               kernel_size=kernel_size,
               padding='valid',
               activation='relu',
               kernel_initializer='glorot_normal',
               strides=1)(input)
            conv_drop = keras.layers.Dropout(0.1)(conv)
            max_pool = keras.layers.MaxPooling1D(3)(conv_drop)
            convs.append(max_pool)
    merge = keras.layers.Concatenate(axis=1)(convs)
    mix = keras.layers.Conv1D(filters=150,
                        kernel_size=3,
                        padding='valid',
                        activation='relu',
                        kernel_initializer='glorot_normal',
                        strides=1)(merge)
    max = keras.layers.MaxPooling1D(3)(mix)
    flatten = keras.layers.Flatten()(max)
    dense = keras.layers.Dense(60, activation='relu')(flatten)
    drop = keras.layers.Dropout(0.5)(dense)
    output = keras.layers.Dense(2, activation='sigmoid')(drop)
    model = tf.keras.Model(inputs=input, outputs=output)
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def create_model_conv_parallel_lstm():
    input = keras.layers.Input(shape=(120, 20))
    kernel_sizes = [3,4,5]
    maps_per_kernel = 2
    convs = []
    for kernel_size in kernel_sizes:
        for map_n in range(maps_per_kernel):
            conv = keras.layers.Conv1D(filters=50,
               kernel_size=kernel_size,
               padding='valid',
               activation='relu',
               kernel_initializer='glorot_normal',
               strides=1)(input)
            conv_drop = keras.layers.Dropout(0.1)(conv)
            max_pool = keras.layers.MaxPooling1D(3)(conv_drop)
            convs.append(max_pool)
    merge = keras.layers.Concatenate(axis=1)(convs)
    mix = keras.layers.Conv1D(filters=150,
                        kernel_size=3,
                        padding='valid',
                        activation='relu',
                        kernel_initializer='glorot_normal',
                        strides=1)(merge)
    max = keras.layers.MaxPooling1D(3)(mix)
    lstm = keras.layers.Bidirectional(keras.layers.LSTM(50, return_sequences=False,
                                                 dropout=0.15, recurrent_dropout=0.15, implementation=0))(max)
    dense = keras.layers.Dense(60, activation='relu')(lstm)
    drop = keras.layers.Dropout(0.5)(dense)
    output = keras.layers.Dense(2, activation='sigmoid')(drop)
    model = tf.keras.Model(inputs=input, outputs=output)
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def create_model_conv():
    model = Sequential([
        keras.layers.Input(shape=(120, 20)),
        keras.layers.Conv1D(filters=50,
               kernel_size=5,
               padding='valid',
               activation='relu',
               kernel_initializer='glorot_normal',
               strides=1),
        keras.layers.Dropout(0.1),
        keras.layers.Conv1D(filters=50,
                            kernel_size=3,
                            padding='valid',
                            activation='relu',
                            kernel_initializer='glorot_normal',
                            strides=1),
        keras.layers.Dropout(0.1),
        keras.layers.Conv1D(filters=150,
                            kernel_size=3,
                            padding='valid',
                            activation='relu',
                            kernel_initializer='glorot_normal',
                            strides=1),
        keras.layers.Dropout(0.1),
        keras.layers.MaxPooling1D(pool_size=2),
        keras.layers.Flatten(),
        keras.layers.Dense(40, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(2, activation='sigmoid')])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def create_model_conv_lstm():
    model = Sequential([
        keras.layers.Input(shape=(120, 20)),
        keras.layers.Conv1D(filters=50,
               kernel_size=5,
               padding='valid',
               activation='relu',
               kernel_initializer='glorot_normal',
               strides=1),
        keras.layers.Dropout(0.1),
        keras.layers.Conv1D(filters=50,
                            kernel_size=3,
                            padding='valid',
                            activation='relu',
                            kernel_initializer='glorot_normal',
                            strides=1),
        keras.layers.Dropout(0.1),
        keras.layers.Conv1D(filters=150,
                            kernel_size=3,
                            padding='valid',
                            activation='relu',
                            kernel_initializer='glorot_normal',
                            strides=1),
        keras.layers.Dropout(0.1),
        keras.layers.MaxPooling1D(pool_size=2),
        keras.layers.Bidirectional(keras.layers.LSTM(60, return_sequences=False,
                                                     dropout=0.15, recurrent_dropout=0.15, implementation=0)),
        keras.layers.Dense(40, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(2, activation='sigmoid')])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def create_model_lstm():
    #### needs uniform hot vector matrix
    model = Sequential([
        keras.layers.Input(shape=(120, 20)),
        keras.layers.Masking(mask_value=0., input_shape=(120, 20)),
        keras.layers.Bidirectional(keras.layers.LSTM(60, return_sequences=False,
                                                     dropout=0.15, recurrent_dropout=0.15, implementation=0)),
        keras.layers.Dense(40, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(2, activation='sigmoid')])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def create_model_embedded_lstm():
    #### needs uniform hot vector matrix
    model = Sequential([
        keras.layers.Embedding(21,128),
        keras.layers.Bidirectional(keras.layers.LSTM(64, return_sequences=False, dropout=0.15,
                                                     recurrent_dropout=0.15, implementation=0)),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(2, activation='sigmoid')])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

def create_model_sequential_lstm():
    #### needs uniform hot vector matrix
    model = Sequential([
        keras.layers.Input(shape=(18, 20)),
        keras.layers.Bidirectional(keras.layers.LSTM(60, return_sequences=True,
                                                     dropout=0.15, recurrent_dropout=0.15, implementation=0)),
        keras.layers.Dropout(0.5),
        keras.layers.TimeDistributed(keras.layers.Dense(1, activation='sigmoid'))])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model