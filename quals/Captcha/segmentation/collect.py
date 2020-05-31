import requests
import os
import time
import cv2
import base64
from PIL import Image
import string
from threading import Thread, Lock
import sys
from queue import Queue
import time
import random

def collect():
    s = requests.Session()
    url = "http://hax1.allesctf.net:9200"
    base="/app/segmentation/train/temp"
    r = s.get(url+"/captcha/0")
    imb64 = r.text.split('<form action="" method="post">')[1].split('<img src="')[1].split('">')[0].split("base64,")[1]
    im = base64.decodebytes(imb64.encode())
    try:
        os.makedirs(base+"/failed")
    except:
        pass
    base_name = ''.join(random.choices(string.ascii_lowercase,k=5))
    name = base+"/%s.bmp" %(base_name)
    with open(name, "wb") as f:
        f.write(im)

    r = s.post(url+"/captcha/0",data={'0':''})
    solution =r.text.split('The solution would have been <b>')[1].split('</b>')[0]

    image = cv2.imread(name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.copyMakeBorder(gray, 8, 8, 8, 8, cv2.BORDER_CONSTANT,value=(255,255,255))
    gray[gray > 40] = 255

    #image = cv2.copyMakeBorder(image, 8, 8, 8, 8, cv2.BORDER_CONSTANT,value=(255,255,255))
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    
    regions = {}

    tolerance = 5
    last = -1

    for cnt in cnts:
        (x, y, w, h) = cv2.boundingRect(cnt)
        if w*h < 4:
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
        #cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 1)
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


    #cv2.imwrite(name+".bmp", image)

    i = 0
    

    try:
        os.makedirs("/app/segmentation/train/1")
    except:
        pass
    try:
        os.makedirs("/app/segmentation/train/2")
    except:
        pass
    b=0
    bk =-1
    bn = 0
    for k in sorted(regions):
        

        x, y, w, h = regions[k]
        letter = gray[y-2:y + h+2, x-2 :x + w +2 ]
        name = "/app/segmentation/train/1/%c_%s.bmp" %(solution[i],''.join(random.choices(string.ascii_lowercase,k=4)))

        if w/h >b:
            b= w/h
            bk =k
            bn = name

        i+=1

        cv2.imwrite(name, letter)
    if len(solution) != len(regions.keys()):
        os.remove(bn)
        x, y, w, h = regions[bk]
        letter = gray[y-2:y + h+2, x-2 :x + w +2 ]
        name = "/app/segmentation/train/2/%c_%s.bmp" %(solution[i],''.join(random.choices(string.ascii_lowercase,k=4)))
        cv2.imwrite(name, letter)

        return
 
   
concurrent = 40
n = 10000
q = Queue(concurrent)
def worker():
    while True:    
        q.get()()
        q.task_done()
        time.sleep(0.05)

for i in range(concurrent):
    t = Thread(target=worker)
    t.daemon = True
    t.start()
try:
    for i in range(n):
        q.put(collect)
        print("[%d/%d]" %(i,n))
    while not q.empty():
        print("[%d/%d]" %(n-q.qsize(),n))
        time.sleep(0.1)
    q.join()
except KeyboardInterrupt:
    sys.exit(1)