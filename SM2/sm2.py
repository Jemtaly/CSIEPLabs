#!/usr/bin/python3
import sys, random
sys.setrecursionlimit(0x10000)
def exgcd(a, b):
    if b == 0:
        return a, (1, 0)
    d, (x, y) = exgcd(b, a % b)
    return d, (y, x - a // b * y)
def isprime(n):
    if n == 2:
        return True
    if n < 2 or n & 1 == 0:
        return False
    for _ in range(16):
        a = random.randrange(1, n)
        d = n - 1
        while d & 1 == 0:
            t = pow(a, d, n)
            if t == n - 1:
                break
            if t != 1:
                return False
            d >>= 1
    return True
def randprime(l):
    while True:
        r = random.getrandbits(l)
        if isprime(r):
            return r
class EC:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
    def check(self, P):
        return not P or (P[0] * P[0] * P[0] - P[1] * P[1] + self.a * P[0] + self.b) % self.p == 0
    def add(self, P, Q):
        if not P:
            return Q
        if not Q:
            return P
        if P[0] == Q[0]:
            if (P[1] + Q[1]) % self.p == 0:
                return
            lmd = (3 * P[0] * Q[0] + self.a) * pow(P[1] + Q[1], self.p - 2, self.p) % self.p
        else:
            lmd = (Q[1] - P[1]) * pow(Q[0] - P[0], self.p - 2, self.p) % self.p
        x = (lmd * lmd - P[0] - Q[0]) % self.p
        y = (lmd * (P[0] - x) - Q[0]) % self.p
        return x, y
    def mult(self, P, n):
        if n == 0:
            return
        Q = self.mult(P, n >> 1)
        return self.add(self.add(Q, Q), P) if n & 1 else self.add(Q, Q)
