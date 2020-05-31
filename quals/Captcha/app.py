import requests
import os
import time
import cv2
import base64
from PIL import Image
import solve
import random
import string
from io import BytesIO
import time
import json

s = requests.Session()
url = "http://hax1.allesctf.net:9200"
base = "/app"


def do(data,stage):
    st = time.perf_counter()
    im = base64.decodebytes(data.encode())
    try:
        os.makedirs(base+("/temp/%d"%stage))
    except:
        pass
    name = base+"/temp/%d/%s.bmp" %(stage,''.join(random.choices(string.ascii_lowercase,k=10)))
    with open(name, "wb") as f:
        f.write(im)
    sol = solve.solve(name)
    #print((time.perf_counter()-st))
    return sol

class Stage:
    def __init__(self,s,url):
        self.url = url
        self.s =s

    def run(self):
        pass

class StageN(Stage):

    def run(self,stage):
        r = s.get(url+"/captcha/%d.html" %(stage))
        if stage == 4:
            print(r.text)
        pics = r.text.split('<form action="" method="post">')[1].split('<img src="')
        payload = {}
        for idx,p in enumerate(pics):
            if idx == 0:
                continue
            payload[idx-1]=do(p.split('">')[0].split("base64,")[1],stage)
        if stage==3:
            wd = r.text
            for idx, p in payload.items():
                wd = wd.replace('<input type="text" name="%d">' %idx, '<input type="text" name="%d" value="%s">'%(idx,p))
            #with open("/app/data.json","w") as f:
            #    f.write(json.dumps(payload))
            with open("/app/data.html","w") as f:
                f.write(wd)
            
            #screenshot(s,url+"/captcha/%d.html" %(stage))
        r = s.post(url+"/captcha/%d.html" %(stage),data=payload)
        
        if "Human detected" in r.text:
            print("failed stage %d" %stage)
            #print(payload)
            #print(r.text)
            #exit(1)
            return False
        return StageN(s,url).run(stage+1)

class Stage0(Stage):

    def run(self):
        r = s.get(url+"/captcha/0")
        imb64 = r.text.split('<form action="" method="post">')[1].split('<img src="')[1].split('">')[0].split("base64,")[1]

        solution = do(imb64,0)
        r = s.post(url+"/captcha/0",data={
            '0':solution
        })
        text = r.text
        if not "Since you are thankfully not humans" in text or not StageN(s,url).run(1):
            if "The solution would have been" in text:
                #print(r.text)
                real =text.split('The solution would have been <b>')[1].split('</b>')[0]
                print("---------\n%s\n%s\n---------" % (solution,real))
            Stage0(s,url).run()
        return True
Stage0(s,url).run()
driver.quit()
