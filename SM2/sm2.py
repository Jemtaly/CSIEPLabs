import random
import pysmx


def kdf(zin, klen):
    rcnt = (klen - 1) // 32 + 1
    ha = b''.join(pysmx.SM3.digest(zin + ct.to_bytes(4, 'big'))
                  for ct in range(1, rcnt + 1))
    return ha[:klen]


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


class SM2:
    def __init__(self, m, a, b, p, n, G):
        self.m = m
        assert isprime(p) and 2 < p < 256 ** m and \
            (4 * a * a * a + 27 * b * b) % p != 0
        self.a = a % p
        self.b = b % p
        self.p = p
        assert isprime(n) and n > 2 ** 191 and n * n > 16 * p and \
            self.check(G) and self.mult(n, G) == None
        self.n = n % p
        self.G = G[0] % p, G[1] % p
        self.d = random.randrange(1, n - 1)
        self.P = self.mult(self.d, G)

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
            lmd = (3 * P[0] * Q[0] + self.a) * \
                pow(P[1] + Q[1], self.p - 2, self.p) % self.p
        else:
            lmd = (Q[1] - P[1]) * pow(Q[0] - P[0], self.p - 2, self.p) % self.p
        x = (lmd * lmd - P[0] - Q[0]) % self.p
        y = (lmd * (P[0] - x) - P[1]) % self.p
        return x, y

    def mult(self, n, P):
        if n == 0:
            return
        Q = self.mult(n >> 1, P)
        return self.add(self.add(Q, Q), P) if n & 1 else self.add(Q, Q)

    def sign(self, M):
        e = int.from_bytes(M, 'big')
        r = 0
        while r == 0 or r + k == self.n or s == 0:
            k = random.randrange(1, self.n)
            x = self.mult(k, self.G)[0]
            r = (e + x) % self.n
            s = pow(self.d + 1, self.n - 2, self.n) * (k - r * self.d) % self.n
        return r.to_bytes(self.m, 'big') + s.to_bytes(self.m, 'big')

    def verify(self, S, M):
        r = int.from_bytes(S[:self.m], 'big')
        s = int.from_bytes(S[self.m:], 'big')
        if not (0 < r < self.n and 0 < s < self.n):
            return False
        e = int.from_bytes(M, 'big')
        t = (r + s) % self.n
        if t == 0:
            return False
        x = self.add(self.mult(s, self.G), self.mult(t, self.P))[0]
        R = (e + x) % self.n
        return r == R

    def encrypt(self, M):
        klen = len(M)
        t = bytes(klen)
        while not any(t):
            k = random.randrange(1, self.n)
            kP = self.mult(k, self.P)
            x2, y2 = kP[0].to_bytes(self.m, 'big'), kP[1].to_bytes(self.m, 'big')
            t = kdf(x2 + y2, klen)
        kG = self.mult(k, self.G)
        x1, y1 = kG[0].to_bytes(self.m, 'big'), kG[1].to_bytes(self.m, 'big')
        C1 = x1 + y1
        C2 = bytes(a ^ b for a, b in zip(M, t))
        C3 = pysmx.SM3.digest(x2 + M + y2)
        return C1 + C2 + C3

    def decrypt(self, C):
        l2 = 2 * self.m
        C1 = C[:l2]
        C2 = C[l2:-32]
        C3 = C[-32:]
        klen = len(C2)
        x1, x2 = C1[:self.m], C1[self.m:]
        kG = int.from_bytes(x1, 'big'), int.from_bytes(x2, 'big')
        kP = self.mult(self.d, kG)
        x2, y2 = kP[0].to_bytes(self.m, 'big'), kP[1].to_bytes(self.m, 'big')
        t = kdf(x2 + y2, klen)
        assert any(t)
        M = bytes(a ^ b for a, b in zip(C2, t))
        assert pysmx.SM3.digest(x2 + M + y2) == C3
        return M
