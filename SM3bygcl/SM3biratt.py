from random import *
from gmssl import sm3
DLEN = 8
def s2l(s):
    return [int(s[i], base = 16) for i in range(0,64)]

def birthday():
    x = [randint(0, 2 ** 32)]
    h = dict()
    temp = x[:]
    while(1):
        m = temp[:]
        temp = sm3.sm3_hash(temp)
        if (temp[0:DLEN] in h):
            break
        h[temp[0:DLEN]] = m
        temp = s2l(temp)
    print("when finding the collision, the amount of hashvalue set : ", len(h))
    print("the collision hash value is : ", temp)
    print("Ma : ", m)
    mb = h[temp[0:DLEN]]
    print("Mb : ", mb)
    realhasha = sm3.sm3_hash(m)
    realhashb = sm3.sm3_hash(mb)
    print("the real hash value of Ma : ", realhasha)
    print("the real hash value of Mb : ", realhashb)
    if realhasha[0:DLEN] == realhashb[0:DLEN]:
        print("True")


if __name__ == "__main__":
    birthday()
