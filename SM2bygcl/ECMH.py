import hashlib
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
G = 0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7, 0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0

# y ^ 2 = x ^ 3 + a * x + b (mod p)
def modular_sqrt(a, p):  # copied by https://eli.thegreenplace.net/2009/03/07/computing-modular-square-roots-in-python
    """ Find a quadratic residue (mod p) of 'a'. p
        must be an odd prime.

        Solve the congruence of the form:
            x^2 = a (mod p)
        And returns x. Note that p - x is also a root.

        0 is returned is no square root exists for
        these a and p.

        The Tonelli-Shanks algorithm is used (except
        for some simple cases in which the solution
        is known from an identity). This algorithm
        runs in polynomial time (unless the
        generalized Riemann hypothesis is false).
    """
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    s = p - 1
    e = 0
    while s % 2 == 0:
        s /= 2
        e += 1
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def legendre_symbol(a, p):    # copied by https://eli.thegreenplace.net/2009/03/07/computing-modular-square-roots-in-python
    """ Compute the Legendre symbol a|p using
        Euler's criterion. p is a prime, a is
        relatively prime to p (if p divides
        a, then a|p = 0)

        Returns 1 if a has a square root modulo
        p, -1 otherwise.
    """
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls


def ECMH(u):
    h = int(hashlib.sha256(str(u).encode()).hexdigest(), 16)
    i = 0
    while(1):
        x = h + i
        d = (x ** 3 + a * x + b) % p
        if pow(d, (p - 1) // 2, p) % p == 1:
            y = modular_sqrt(d, p)
            return [x, y]

def ECMH_set(s):
    s = set(s)
    result = [0, 0]
    for x in s:
        result[0] += ECMH(x)[0]
        result[1] += ECMH(x)[1]
    return result

if __name__ == '__main__':
    m1 = '123'
    h1 = ECMH(m1)
    print("ECMH('{}') = {}".format(m1, h1))
    m2 = '789'
    h2 = ECMH(m2)
    print("ECMH('{}') = {}".format(m2, h2))
    s1 = {m1, m2}
    h3 = ECMH_set(s1)
    print("ECMH({}) = {}".format(s1, h3))
    if (h3[0] == h2[0] + h1[0] and h3[1] == h2[1] + h1[1]):
        print("ECMH('{}') + ECMH('{}') == ECMH({})".format(m1, m2, s1))
    s3 = s1 - {m1}
    h3 = ECMH_set(s3)
    print("ECMH({} - {}) = {}".format(s1, {m1}, h3))
    if(h3 == h2):
        print("ECMH({} - {}) == ECMH('{}')".format(s1, {m1}, m2))

