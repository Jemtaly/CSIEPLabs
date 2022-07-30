from re import T
from gmssl import sm2, sm4, sm3, func
import random
from Crypto.Util.number import *
import hashlib
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
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

salt = get_random_bytes(32)

def SM2_Encrypt(m, d1, d2):
    klen = len(m)
    P = mult(inverse(d1 * d2, n) - 1, G)
    d = inverse(d1 * d2, n) - 1
    k = random.randint(1, n - 1)
    C1 = mult(k, G)
    kP = mult(k, P)
    x2, y2 = kP
    t = int(scrypt(str(kP[0])+str(kP[1]), salt, 32, N = 2 ** 14, r = 8, p = 1).hex(), 16)
    C2 = hex(int(str(m).encode('utf-8').hex(),16) ^ t)[2:]
    C3 = sm3.sm3_hash(func.bytes_to_list(bytes(str(x2) + str(m) + str(y2), encoding = 'utf-8')))
    return (C1, C2, C3)
    

d1 = 14628408464009883489095773347787361334036808351949278760972164281293629470247
d2 = 10481462233935693906729851923940092144349235314874115506744237748052506715299
m = 'hello, fixedpoint'
print("m = ")
print(m)
C1, C2, C3 = SM2_Encrypt(m, d1, d2)
print("generate sub private key d1 : ")
print(d1)
print("ciphertext = ")
print(C1, C2, C3)
if (C1 == 0):
    print("error")
else:
    T1 = mult(inverse(d1, n), C1)

print("compute T1 = ")
print(T1)
s.sendto(str(T1[0]).encode(), Baddress)
s.sendto(str(T1[1]).encode(), Baddress)

T2x = int(s.recvfrom(1024)[0].decode(), 10)
T2y = int(s.recvfrom(1024)[0].decode(), 10)
T2 = [T2x, T2y]

InvC1 = [C1[0], -C1[1]]
x2, y2 = add(T2, InvC1)
t = int(scrypt(str(x2)+str(y2), salt, 32, N = 2 ** 14, r = 8, p = 1).hex(), 16)
M_ = hex(int(C2, 16) ^ t)[2:]
M_ = bytes().fromhex(M_).decode('utf-8')
u = sm3.sm3_hash(func.bytes_to_list(bytes(str(x2) + str(M_) + str(y2), encoding = 'utf-8')))
if u == C3:
    print("Decrypt success")
    print("M'' = ")
    print(M_)