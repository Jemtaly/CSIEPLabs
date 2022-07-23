from numpy import *
import random
from Crypto.Util.number import * 
import hashlib
# y ^ 2 = x ^ 3 + a * x + b (mod p)
a = 2
b = 2
p = 17

def ECCADD(P, Q):
    if (P[0] == 0) and (P[1] == 0):
        return Q
    if (Q[0] == 0) and (Q[1] == 0):
        return P
    if (P == Q):
        lambd = ((3 * (P[0] ** 2) + a ) * inverse(2 * P[1], p)) % p
    else:
        if gcd(Q[0] - P[0], p) != 1 and gcd(Q[0] - P[0], p) != -1:
            return [0, 0]
        else:
            lambd = ((Q[1] - P[1]) * inverse(Q[0] - P[0], p)) % p
    x = (lambd ** 2 - P[0] - Q[0]) % p
    y = (lambd * (P[0] - x) - P[1]) % p
    return [x,y]

def ECCMUL(k, Q):
    if k == 0:
        return [0,0]
    if k == 1:
        return Q
    if k >= 2:
        temp = Q
        while(1):
            temp = ECCADD(temp, Q)
            k = k - 1
            if k == 1:
                return temp



def ECDSASign(d, e, n, G):  #e = hash(m)
    while 1:
        k = random.randint(1, n)
        if gcd(k, n) == 1:
            break
    R = ECCMUL(k, G)
    r = R[0] % n
    s = (((inverse(k, n)+n)%n) * (e + d * r)) % n
    return [r, s]

def ECDSAVrfy(P, e, n, G, r, s):  #e = hash(m)
    w = (inverse(s, n) + n) % n
    t1 = (e * w) % n
    t2 = (r * w) % n
    X = ECCADD(ECCMUL(t1, G), ECCMUL(t2, P))
    r_ = X[0]
    if r == r_:
        return 1
    else:
        return 0

def pretend(G, P, n):
    u = random.randint(1, n)
    v = random.randint(1, n)
    R = ECCADD(ECCMUL(u, G), ECCMUL(v, P))
    r = R[0] % n
    e = (r * u * inverse(v, n)) % n
    s = (r * inverse(v, n)) % n
    return e, r, s

if __name__ == '__main__':
    m = '123'
    G = [5, 1]
    n = 19
    d = 5
    P = ECCMUL(d, G)
    print(P)
    e = int(hashlib.sha256(str(m).encode()).hexdigest(),base = 16)
    print(e)
    S = ECDSASign(d, e, n, G)
    r = S[0]
    s = S[1]
    print(S)
    if ECDSAVrfy(P, e, n, G, r, s) == 1:
        print("SignVrfy pass")
    e_, r_, s_ = pretend(G, P, n)
    print("forge signature: hash(m') = {}, r' = {}, s' = {}".format(e_, r_, s_))
    if ECDSAVrfy(P, e_, n, G, r_, s_) == 1:
        print("forged SignVrfy pass")


