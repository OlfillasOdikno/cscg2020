import OpenSSL.crypto as crypto
from factordb.factordb import FactorDB

def read_key(f):
    return crypto.load_publickey(crypto.FILETYPE_PEM,open(f,"rb").read()).to_cryptography_key().public_numbers()

keyD = read_key("german_government.pem")
keyU =  read_key("us_government.pem")
keyR = read_key("russian_government.pem")

messages = [int(l.split(": ")[1]) for l in open("intercepted-messages.txt","rb").readlines()]

cD = messages[0]
cU = messages[1]
cR = messages[2]

assert(keyD.e==keyU.e==keyR.e==3)

M = crt([cD,cU,cR],[keyD.n,keyU.n,keyR.n]).nth_root(3)
print(hex(int(str(M))).replace("L","")[2:].decode('hex'))
