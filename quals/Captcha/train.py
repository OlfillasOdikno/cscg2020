from glob import glob
import cv2
import numpy as np
import pickle
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense, Dropout
from keras.callbacks import EarlyStopping
import os
data = []
labels = []

    
os.makedirs("/app/model",exist_ok=True)

dirs = glob("/app/train/*/")
dirs = list(filter(lambda x: 'temp' != x.split('/')[-2],dirs))

for j,d in enumerate(dirs):
    l = d.split("/")[-2]
    files = glob(d+"/*")
    for k,f in enumerate(files):
        print('\r[dir: %d/%d file:%d/%d]' %(j,len(dirs),k,len(files)),end='')
        img = cv2.imread(f)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (20, 20))
        img = np.expand_dims(img, axis=2)
        data.append(img)
        labels.append(l)
print('[*] done')

data = np.array(data, dtype="float") / 255.0

print("[*] Training for %d chars" % (len(dirs)))

(X_train, X_test, Y_train, Y_test) = train_test_split(data, np.array(labels), test_size=0.40, random_state=0)

lb = LabelBinarizer().fit(Y_train)
Y_train = lb.transform(Y_train)
Y_test = lb.transform(Y_test)

print("[*] writing labels")
with open("/app/model/labels.dat", "wb") as f:
    pickle.dump(lb,f)
print("[*] done!")

print("[*] building model")

early_stop = EarlyStopping(monitor='val_loss', min_delta=0, patience=3, verbose=1, mode='auto')

model = Sequential()

model.add(Conv2D(20, (5, 5), padding="same", input_shape=(20, 20, 1), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Conv2D(50, (5, 5), padding="same", activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

model.add(Flatten())
model.add(Dense(500, activation="relu"))
model.add(Dropout(0.5, name='dropout_1'))

model.add(Dense(len(dirs), activation="softmax"))

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
print("[*] done!")

print("[*] start training")
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), batch_size=len(dirs), epochs=10, verbose=1,callbacks=[early_stop  ])

print("[*] done!")

print("[*] saving model")
model.save("/app/model/model.hdf5")
print("[*] done!")