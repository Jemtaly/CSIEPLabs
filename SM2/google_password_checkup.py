import random


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


class GPCServer:
    def __init__(self, data, p):
        assert isprime(p)
        self.p = p
        self.b = random.randrange(1, self.p)
        self.table = {i.to_bytes(2, 'big'): set() for i in range(0xffff)}
        for up in data.items():
            h = hash(up) % self.p
            k = h.to_bytes(8, 'big')[:2]
            v = pow(h, self.b, self.p)
            self.table[k].add(v)

    def find_S(self, k, v):
        hab = pow(v, self.b, self.p)
        S = self.table[k]
        return hab, S


class GPCClient:
    def __init__(self, up, p):
        assert isprime(p)
        self.p = p
        self.h = hash(up) % self.p
        phi = self.p - 1
        while True:
            self.a = random.randrange(0, phi)
            gcd, (r, _) = exgcd(self.a, phi)
            if gcd == 1:
                self.r = r % phi
                break

    def get_kv(self):
        k = self.h.to_bytes(8, 'big')[:2]
        v = pow(self.h, self.a, self.p)
        return k, v

    def detect(self, hab, S):
        hb = pow(hab, self.r, self.p)
        return hb in S

def main():
    p = randprime(64)
    data = {random.randbytes(4): random.randbytes(8) for _ in range(10)}
    user_1 = (random.randbytes(4), random.randbytes(8))
    user_2 = data.popitem()
    data.update([user_1])
    server = GPCServer(data, p)
    client_1 = GPCClient(user_1, p)
    client_2 = GPCClient(user_2, p)
    valid_1 = client_1.detect(*server.find_S(*client_1.get_kv()))
    valid_2 = client_2.detect(*server.find_S(*client_2.get_kv()))
    print('data:')
    for user in data.items():
        print('u = ' + user[0].hex() + ', p = ' + user[1].hex())
    print()
    print('user_1:')
    print('u = ' + user_1[0].hex() + ', p = ' + user_1[1].hex())
    print('user_1 is', 'valid.' if valid_1 else 'invalid.')
    print()
    print('user_2:')
    print('u = ' + user_2[0].hex() + ', p = ' + user_2[1].hex())
    print('user_2 is', 'valid.' if valid_2 else 'invalid.')

if __name__ == '__main__':
    main()
