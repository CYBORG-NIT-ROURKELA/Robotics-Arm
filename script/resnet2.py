# -*- coding: utf-8 -*-
"""ResNet2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1H5GC-rPqHVtSYwSnDF3wJZIJ5dfk4yup
"""

import numpy as np
import os
import time
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.applications.imagenet_utils import decode_predictions
from keras.layers import Dense, Activation, Flatten
from keras.layers import merge, Input
from keras.models import Model,Sequential
from keras.utils import np_utils
from sklearn import preprocessing
from keras.layers import *
from keras.models import *
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Normalizer
from keras.layers import Convolution2D, GlobalAveragePooling2D,Dropout
from keras.layers.recurrent import LSTM
import glob
from keras import optimizers
from keras.applications.resnet50 import ResNet50

from google.colab import drive
drive.mount('/content/drive', force_remount = True)

X_data1_test = []
image = np.empty(48, dtype=object)
files = glob.glob("/content/drive/My Drive/ALL/ALL_IDB2/img0_test/*.tif")
for myFile in files:
  image = cv2.imread(myFile)
  x_img1_test = cv2.resize(image,(224,224),interpolation = cv2.INTER_CUBIC)
  X_data1_test.append(x_img1_test)
print(np.array(X_data1_test).shape)

X_data2_test = []
image = np.empty(48, dtype=object)
files = glob.glob("/content/drive/My Drive/ALL/ALL_IDB2/img1_test/*.tif")
for myFile in files:
  image = cv2.imread(myFile)
  x_img2_test = cv2.resize(image,(224,224),interpolation = cv2.INTER_CUBIC)
  X_data2_test.append(x_img2_test)
print(np.array(X_data2_test).shape)

X_data1_train = []
image = np.empty(48, dtype=object)
files = glob.glob("/content/drive/My Drive/ALL/ALL_IDB2/img0_train/*.tif")
for myFile in files:
  image = cv2.imread(myFile)
  x_img1_train = cv2.resize(image,(224,224),interpolation = cv2.INTER_CUBIC)
  X_data1_train.append(x_img1_train)
print(np.array(X_data1_train).shape)

X_data2_train = []
image = np.empty(48, dtype=object)
files = glob.glob("/content/drive/My Drive/ALL/ALL_IDB2/img1_train/*.tif")
for myFile in files:
  image = cv2.imread(myFile)
  x_img2_train = cv2.resize(image,(224,224),interpolation = cv2.INTER_CUBIC)
  X_data2_train.append(x_img2_train)
print(np.array(X_data2_train).shape)

for i in X_data2_test:
  X_data1_test.append(i)
for j in X_data2_train:
  X_data1_train.append(j)

print(np.array(X_data1_train).shape) 
print(np.array(X_data1_test).shape)

labels1 = np.ones(len(X_data1_train),dtype='int64')
labels1[0:89] = 0
labels1[90:] = 1
labels2 = np.ones(len(X_data1_test),dtype='int64')
labels2[0:39] = 0
labels2[40:] = 1

X_train = X_data1_train
X_train = np.array(X_train)
X_test = X_data1_test
X_test = np.array(X_test)
Y_train = np_utils.to_categorical(labels1, 2)
Y_train = np.array(Y_train)
Y_test = np_utils.to_categorical(labels2, 2)
Y_test = np.array(Y_test)

base_model = ResNet50(weights= 'imagenet', include_top=False, input_shape= (224,224,3))
base_model.summary()

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
predictions = Dense( 2 , activation= 'softmax')(x)
model = Model(inputs = base_model.input, outputs = predictions)

model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['accuracy'])

from keras.callbacks import EarlyStopping,ReduceLROnPlateau,ModelCheckpoint
callbacks = [
    EarlyStopping(patience=10, verbose=1),
    ReduceLROnPlateau(factor=0.6, patience=6, min_lr=0.000001, verbose=1),
    ModelCheckpoint('/content/drive/My Drive/Colab Notebooks/model-ResNet502.h5', verbose=1, save_best_only=True)
]

t=time.time()
#	t = now()
hist = model.fit(X_train, Y_train, batch_size=16, epochs=20, verbose=1,callbacks = callbacks, validation_data=(X_test, Y_test))
print('Training time: %s' % (t - time.time()))
(loss, accuracy) = model.evaluate(X_test, Y_test, batch_size=4, verbose=1)

print("[INFO] loss={:.4f}, accuracy: {:.4f}%".format(loss,accuracy * 100))