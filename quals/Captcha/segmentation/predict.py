from keras.models import load_model
import numpy as np
import cv2
import pickle

with open("/app/segmentation/model/labels.dat", "rb") as f:
    lb = pickle.load(f)

model = load_model("/app/segmentation/model/model.hdf5")

def is_two(img):
    height, width = img.shape[:2]
    w_ = round(20*(width/height))
    img = cv2.resize(img,(w_,20))
    img = cv2.copyMakeBorder(img, 0, 0, max((40-w_)//2,0), max((40-w_)//2,0), cv2.BORDER_CONSTANT,value=(255,255,255))

    img = cv2.resize(img, (40, 20))
    img = np.expand_dims(img, axis=2)
    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)
    c = lb.inverse_transform(prediction)[0]
    return int(c)
