from keras.models import load_model
import numpy as np
import cv2
import pickle
import segmentation.predict as predict
with open("/app/model/labels.dat", "rb") as f:
    lb = pickle.load(f)

model = load_model("/app/model/model.hdf5")

def solve(name):
    image = cv2.imread(name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_CONSTANT,value=(255,255,255))
    gray[gray > 60] = 255

    #image = cv2.copyMakeBorder(image, 8, 8, 8, 8, cv2.BORDER_CONSTANT,value=(255,255,255))
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    
    regions = {}

    tolerance = 5
    last = -1

    for cnt in cnts:
        (x, y, w, h) = cv2.boundingRect(cnt)
        if (w*h <= 3**2 and w/h == 1) or w*h < 7:
            continue
        if x in regions:
            (x1, y1, w1, h1) = regions[x]
            x_ = min(x,x1)
            y_ = min(y,y1)
            ww_ = max(x+w,x1+w1)
            hh_ = max(y+h,y1+h1)
            regions[x]=(x_,y_,ww_-x_,hh_-y_)
            continue
        regions[x]=(x,y,w,h)
    for k in sorted(regions):
        (x, y, w, h) = regions[k]
        if last >= 0:
            (x1, y1, w1, h1) = regions[last]
            if ((abs(1-w/h) < 0.35 and w <8 and h <8) or (abs(1-w1/h1) < 0.35) and w1 <8 and h1 <8):
                if x < x1 + w1 +tolerance and  x + w +tolerance > x1:
                    x_ = min(x,x1)
                    y_ = min(y,y1)
                    ww_ = max(x+w,x1+w1)
                    hh_ = max(y+h,y1+h1)
                    regions[last]=(x_,y_,ww_-x_,hh_-y_)
                    del regions[k]
                    #cv2.rectangle(image, (x_,y_), (ww_,hh_), (255, 255, 0), 1)
                    continue
            elif x < x1 + w1 and x + w > x1:
                x_ = min(x,x1)
                y_ = min(y,y1)
                ww_ = max(x+w,x1+w1)
                hh_ = max(y+h,y1+h1)
                regions[last]=(x_,y_,ww_-x_,hh_-y_)
                del regions[k]
                #cv2.rectangle(image, (x_,y_), (ww_,hh_), (255, 255, 0), 1)
                continue

        regions[x]=(x, y, w, h)
        last = x
            #cv2.rectangle(image, (x,y), (w,h), (255, 0, 0), 1)

    for k in sorted(regions):
        (x, y, w, h) = regions[k]
        letter = gray[y-2:y + h+2, x-2 :x + w +2 ]
        n = predict.is_two(letter)
        if n == 2:
            hw = w // 2
            regions[x]=(x, y, hw, h)
            regions[x+hw]=(x + hw, y, hw, h)

    ret = []
    for k in sorted(regions):
        x, y, w, h = regions[k]

        letter = gray[y-2:y + h+2, x-2 :x + w +2 ]
        letter = cv2.resize(letter, (20, 20))
        letter = np.expand_dims(letter, axis=2)
        letter = np.expand_dims(letter, axis=0)

        prediction = model.predict(letter)

        c = lb.inverse_transform(prediction)[0]
        ret.append(c)
    return ''.join(ret)

