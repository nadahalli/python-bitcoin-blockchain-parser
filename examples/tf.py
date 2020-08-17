import tensorflow as tf
from tensorflow import keras

import os
import tempfile

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import sklearn
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

file = tf.keras.utils
raw_df = pd.read_csv('t.sampled.csv', sep=';')

def label_split(frame):
    neg, pos = np.bincount(frame)
    total = neg + pos
    print('Examples:\n    Total: {}\n    Positive: {} ({:.2f}% of total)\n'.format(
        total, pos, 100 * pos / total))

cleaned_df = raw_df.copy()

cleaned_df.pop('txid')
cleaned_df.pop('created_block')
cleaned_df.pop('spent_block')
cleaned_df.pop('life')
labels = cleaned_df.pop('label')

x_train, x_test, y_train, y_test = train_test_split(cleaned_df, labels, test_size=0.2)

assert(len(x_train) == len(y_train))
assert(len(x_test) == len(y_test))
label_split(y_train)
label_split(y_test)

scaler = StandardScaler()
train_features = scaler.fit_transform(x_train)
test_features = scaler.transform(x_test)

METRICS = [
      keras.metrics.TruePositives(name='tp'),
      keras.metrics.FalsePositives(name='fp'),
      keras.metrics.TrueNegatives(name='tn'),
      keras.metrics.FalseNegatives(name='fn'), 
      keras.metrics.BinaryAccuracy(name='accuracy'),
      keras.metrics.Precision(name='precision'),
      keras.metrics.Recall(name='recall'),
      keras.metrics.AUC(name='auc'),
]

def make_model(metrics = METRICS, output_bias=None):
  if output_bias is not None:
    output_bias = tf.keras.initializers.Constant(output_bias)
  model = keras.Sequential([
      keras.layers.Dense(
          16, activation='relu',
          input_shape=(x_train.shape[-1],)),
      keras.layers.Dropout(0.5),
      keras.layers.Dense(1, activation='sigmoid',
                         bias_initializer=output_bias),
  ])

  model.compile(
      optimizer=keras.optimizers.Adam(lr=1e-3),
      loss=keras.losses.BinaryCrossentropy(),
      metrics=metrics)

  return model

EPOCHS = 10

model = make_model()
model.fit(x_train, y_train, epochs=EPOCHS)
print(model.summary())
results = model.evaluate(x_test, y_test)

for name, value in zip(model.metrics_names, results):
    print(name, value)

