# -*- coding: utf-8 -*-
"""Proyek_TimeSeries_Millata Tasyakhanifa.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CMqTL8c8mEwQuNNnaXv0zGo_TFMfbX6C

### Nama: Millata Tasyakhanifa
### Username: millatasyaa
### Email: millatatasyakhanifa@gmail.com

## Import Library
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from keras.layers import Dense, LSTM

"""## Read Dataset"""

df = pd.read_csv("/content/GOOG.csv", date_parser=True)

df

df.info()

df.isnull().sum()

"""## Plot Data"""

dates = df['Date'].values
close = df['Close'].values
 
 
plt.figure(figsize=(15,5))
plt.plot(dates, close)
plt.title('Close Price Average',
          fontsize=20);

"""## Drop Unnecessary Column"""

df = df.drop(['Date', 'Adj Close'], axis=1)

df

"""## Scaling Data """

min_max_scaler = MinMaxScaler()
df = min_max_scaler.fit_transform(df)

df

df.shape

X_train =[]
y_train = []

for i in range(30, df.shape[0]):
  X_train.append(df[i-30:i])
  y_train.append(df[i,0])

X_train, y_train = np.array(X_train), np.array(y_train)

X_train.shape

y_train.shape

"""## Build Model"""

model = tf.keras.models.Sequential([
  tf.keras.layers.LSTM(50, activation="relu", return_sequences=True, input_shape=(X_train.shape[1], 5)),
  tf.keras.layers.LSTM(60, activation="relu", return_sequences=True),
  tf.keras.layers.LSTM(80, activation="relu", return_sequences=True),
  tf.keras.layers.Dense(30, activation="relu"),
  tf.keras.layers.Dense(10, activation="relu"),
  tf.keras.layers.Dense(1),
])

model.summary()

optimizer = tf.keras.optimizers.SGD(learning_rate=1.0000e-04, momentum=0.9)
model.compile(loss=tf.keras.losses.Huber(),
              optimizer=optimizer,
              metrics=["mae"])

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('mae')<0.1):
      print("\nMAE dari model telah mencapai < 10% skala data")
      self.model.stop_training = True
callbacks = myCallback()

history = model.fit(X_train, 
                    y_train, 
                    epochs=200,
                    batch_size=128,
                    validation_split=0.2, # Validation set = 20% 
                    callbacks=[callbacks])

"""## Loss and MAE Plots During Training and Validation"""

plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Train and Validation Loss Graphs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.figure(figsize=(18, 6))
plt.plot(history.history['mae'], label='Train MAE')
plt.plot(history.history['val_mae'], label='Validation MAE')
plt.title('Train and Validation MAE Graphs')
plt.xlabel('Epochs')
plt.ylabel('MAE')
plt.legend()