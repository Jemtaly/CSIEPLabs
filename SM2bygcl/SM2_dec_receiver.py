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
APORT = 50002
BPORT = 50003
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

d2 = 10481462233935693906729851923940092144349235314874115506744237748052506715299
print("generate sub private key d2 :")
print(d2)

T1x = int(s.recvfrom(1024)[0].decode(), 10)
T1y = int(s.recvfrom(1024)[0].decode(), 10)

T1 = [T1x, T1y]

T2 = mult(inverse(d2, n), T1)

s.sendto(str(T2[0]).encode(), Aaddress)
s.sendto(str(T2[1]).encode(), Aaddress)