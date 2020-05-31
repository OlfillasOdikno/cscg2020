import OpenSSL.crypto as crypto
from factordb.factordb import FactorDB

key = open("pubkey.pem","rb").read()
message = open("message.txt","rb").read()

key = crypto.load_publickey(crypto.FILETYPE_PEM, key)
numbers = key.to_cryptography_key().public_numbers()

N = numbers.n
E = numbers.e

C = int(message)
def fermat(n):
    a = isqrt(n)
    while True:
        b = a**2-n
        if b > 0 and b.is_square():
            p = int(str(a-isqrt(b)))
            return p,n/p
        a +=1
    
factors = fermat(N)
P = factors[0]
Q = factors[1]
D = xgcd(E,(P - 1) * (Q - 1))[1]
M = pow(C,D,N)
print(hex(int(str(M))).replace("L","")[2:].decode('hex'))
