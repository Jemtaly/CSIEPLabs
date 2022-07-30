from gmssl import sm2, sm4
import random
from Crypto.Util.number import *
import hashlib
import socket

a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
G = 0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7, 0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0


HOST = '127.0.0.1'
APORT = 50000
BPORT = 50001
Aaddress = (HOST, APORT)
Baddress = (HOST, BPORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#UDP
s.bind((HOST, APORT))

def add(P, Q):
        if not P:
            return Q
        if not Q:
            return P
        if P[0] == Q[0]:
            if (P[1] + Q[1]) % p == 0:
                return
            lmd = (3 * P[0] * Q[0] + a) * \
                pow(int(P[1] + Q[1]), p - 2, p) % p
        else:
            lmd = (Q[1] - P[1]) * pow(int(Q[0] - P[0]), p - 2, p) % p
        x = (lmd * lmd - P[0] - Q[0]) % p
        y = (lmd * (P[0] - x) - P[1]) % p
        return x, y
def mult(n, P):
        if n == 0:
            return
        Q = mult(n >> 1, P)
        return add(add(Q, Q), P) if n & 1 else add(Q, Q)


d1 = random.randint(1, n - 1)
P1 = mult(inverse(d1, n), G)
print("generate sub private key : ")
print(d1)
print("P1 = ")
print(P1)
s.sendto(str(P1[0]).encode(), Baddress)
s.sendto(str(P1[1]).encode(), Baddress)
M = 'hello, fixedpoint!'
Z = 'id'
M_ = Z + M
e = hashlib.sha256(M_.encode()).hexdigest()
print("M :")
print(M)
print("Z :")
print(Z)
print("M' = ")
print(M_)
print("hash(M') = ")
print(e)
k1 = random.randint(1, n - 1)
print("randomly generate k1 :")
print(k1)
Q1 = mult(k1, G)
print("compute Q1 = ")
print(Q1)
s.sendto(str(Q1[0]).encode(), Baddress)
s.sendto(str(Q1[1]).encode(), Baddress)
s.sendto(str(k1).encode(), Baddress)

r = int(s.recvfrom(1024)[0].decode(), 10)
print("received r : ")
print(r)
s2 = int(s.recvfrom(1024)[0].decode(), 10)
print("received s2 : ")
print(s2)
s3 = int(s.recvfrom(1024)[0].decode(), 10)
print("received s3 : ", s3)
print(s3)

s = ((d1 * k1) * s2 + d1 *s3 - r) % n
print("compute s = ")
print(s)
if s == 0 and s == n - r:
    print("error")
else:
    sig = [r, s]
    print("signature sig = ")
    print(sig)
