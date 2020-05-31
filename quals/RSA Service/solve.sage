import numpy
from pyasn1.codec.der import encoder
from pyasn1.type.univ import SequenceOf
from pyasn1.type.univ import Integer as CompInt
import base64
import socket
def gen_cand(b,l):
    p = 2
    while log(p)/log(2) < b:
        np = next_prime(numpy.random.randint(2,l))
        p = p*np
    return p+1

def kk(b,l):
    while True:
       p = gen_cand(b,l)
       if is_prime(p):
           return p

M = 1067267517149537754067764973523953846272152062302519819783794287703407438588906504446261381994947724460868747474504670998110717117637385810239484973100105019299532993569
C = 6453808645099481754496697330465

Q = 2
bits = 559

E = 0
while E <3:
  P = kk(bits,10**6)
  N = P*Q
  gp("addprimes(%d)"%(P))
  sol = gp("znlog(%d, Mod(%d, %d))" % (M,C,N))
  if len(sol) == 0:
    continue
  D = Integer(sol)
  try:
    E = inverse_mod(D,(P-1) * (Q-1))
  except:
    continue

P = P.__int__()
Q = Q.__int__()
D = D.__int__()
N = N.__int__()
E = E.__int__()

print("P: %d"%P)
print("Q: %d"%Q)
print("E: %d"%E)
print("D: %d"%D)

seq = SequenceOf(componentType=CompInt())
enc = encoder.encode([0,N,E,D,P,Q,D % (P-1), D % (Q-1), inverse_mod(Q,P).__int__()],asn1Spec=SequenceOf(componentType=CompInt()))
pem = '-----BEGIN RSA PRIVATE KEY-----\n%s\n-----END RSA PRIVATE KEY-----\n' % base64.b64encode(enc)
s = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
s.connect(("hax1.allesctf.net", 9400))
s.recv(1024)
s.send(pem+"\n")
s.recv(1024)
s.send("\n")
print(s.recv(1024))
print(s.recv(1024))