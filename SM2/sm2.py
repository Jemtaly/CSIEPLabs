import random
import pysmx.SM3


def kdf(zin, klen):
    rcnt = (klen - 1) // 32 + 1
    ha = b''
    for ct in range(1, rcnt + 1):
        ha = ha + pysmx.SM3.digest(zin + ct.to_bytes(4, 'big'))
    return ha


class SM2:
    def __init__(self, a, b, n, p, G, paralen):
        self.n = n
        self.a = a
        self.b = b
        self.p = p
        self.G = G
        self.paralen = paralen
        self.d = random.randrange(1, n - 1)
        self.P = self.mult(self.d, G)

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
        return r.to_bytes(self.paralen, 'big') + s.to_bytes(self.paralen, 'big')

    def verify(self, S, M):
        r, s = int.from_bytes(S[:self.paralen], 'big'), int.from_bytes(
            S[self.paralen:], 'big')
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
            x2, y2 = kP[0].to_bytes(self.paralen, 'big'), kP[1].to_bytes(self.paralen, 'big')
            t = kdf(x2 + y2, klen)
        kG = self.mult(k, self.G)
        x1, y1 = kG[0].to_bytes(self.paralen, 'big'), kG[1].to_bytes(self.paralen, 'big')
        C1 = x1 + y1
        C2 = bytes(a ^ b for a, b in zip(M, t))
        C3 = pysmx.SM3.digest(x2 + M + y2)
        return C1 + C2 + C3

    def decrypt(self, C):
        l2 = 2 * self.paralen
        C1 = C[:l2]
        C2 = C[l2:-32]
        C3 = C[-32:]
        klen = len(C2)
        x1, x2 = C1[:self.paralen], C1[self.paralen:]
        kG = int.from_bytes(x1, 'big'), int.from_bytes(x2, 'big')
        kP = self.mult(self.d, kG)
        x2, y2 = kP[0].to_bytes(self.paralen, 'big'), kP[1].to_bytes(self.paralen, 'big')
        t = kdf(x2 + y2, klen)
        assert any(t)
        M = bytes(a ^ b for a, b in zip(C2, t))
        assert pysmx.SM3.digest(x2 + M + y2) == C3
        return M


def test():
    a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    G = 0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7, 0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0
    sm2 = SM2(a, b, n, p, G, 32)
    m = b'abc'
    c = sm2.encrypt(m)
    p = sm2.decrypt(c)
    print('------------------------ Encrypt and Decrypt ------------------------')
    print('m = 0x' + m.hex())
    print('c = 0x' + c.hex())
    print('p = 0x' + p.hex())
    print('Decryption succeeded.' if p == m else 'Decryption failed.')
    print('-------------------------- Sign and Verify --------------------------')
    s = sm2.sign(m)
    print('s = 0x' + s.hex())
    print('Verification succeeded.' if sm2.verify(s, m) else 'Verification failed.')


if __name__ == '__main__':
    test()
