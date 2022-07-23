#!/usr/bin/python3
import sys, random
sys.setrecursionlimit(0x10000)
class EC:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
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