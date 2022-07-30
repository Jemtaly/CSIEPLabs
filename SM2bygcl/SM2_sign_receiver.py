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
s.bind((HOST, BPORT))

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


d2 = random.randint(1, n - 1)
print("generate sub private key : ")
print(d2)
P1x = int(s.recvfrom(1024)[0].decode(), 10)
P1y = int(s.recvfrom(1024)[0].decode(), 10)
P1 = [P1x, P1y]
P = mult(inverse(d2, n), P1)
InvG = [G[0], -G[1]]
P = add(P, InvG)
print("compute P = ")
print(P)

Q1x = int(s.recvfrom(1024)[0].decode(), 10)
Q1y = int(s.recvfrom(1024)[0].decode(), 10)
Q1 = [Q1x, Q1y]
e = int(s.recvfrom(1024)[0].decode(), 10)
k2 = random.randint(1, n - 1)
k3 = random.randint(1, n - 1)
Q2 = mult(k2, G)
TEMP = add(mult(k3, Q1), Q2)
x1 = TEMP[0]
y1 = TEMP[1]
r = (x1 + e) % n
s2 = (d2 * k3) % n
s3 = (d2 * (r + k2)) % n
print("compute r = ")
print(r)
print("compute s2 = ")
print(s2)
print("compute s3 = ")
print(s3)

s.sendto(str(r).encode(), Aaddress)
s.sendto(str(s2).encode(), Aaddress)
s.sendto(str(s3).encode(), Aaddress)
