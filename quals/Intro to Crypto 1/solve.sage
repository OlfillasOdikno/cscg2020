import OpenSSL.crypto as crypto
from factordb.factordb import FactorDB

key = open("pubkey.pem","rb").read()
message = open("message.txt","rb").read()

key = crypto.load_publickey(crypto.FILETYPE_PEM, key)
numbers = key.to_cryptography_key().public_numbers()

N = numbers.n
E = numbers.e
C = int(message)

f = FactorDB(N)
f.connect()
if f.get_status() == "FF":
    factors = f.get_factor_list()
    if len(factors) != 2:
        print("invalid N")
        exit(1)
    P = factors[0]
    Q = factors[1]
    D = xgcd(E,(P - 1) * (Q - 1))[1]
    M = pow(C,D,N)
    print(hex(int(str(M))).replace("L","")[2:].decode('hex'))
else:
    print("Not fully factored")