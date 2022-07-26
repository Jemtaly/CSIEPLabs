from gmssl import sm3
from random import *

DLEN = 4

def s2l(s):
    return [int(s[i], base = 16) for i in range(0,64)]

def Rho():
    start = sm3.sm3_hash([randint(0, 2 ** 32)])
    x = s2l(start)
    h = []
    while(1):
        temp = sm3.sm3_hash(x)
        if (temp[0:DLEN] in h):
            break
        h.append(temp[0:DLEN])
        temp = s2l(temp)
    l = len(h)
    print(l)
    print("find the loop. The length of loop is {}".format(l))
    x = s2l(start)
    y = s2l(start)
    for i in range(l):
        x = sm3.sm3_hash(x)
        x = s2l(x)
    print(x)
    while(1):
        x = sm3.sm3_hash(x)
        y = sm3.sm3_hash(y)
        if(x[0:DLEN] == y[0:DLEN]):
            return [tempx, tempy]
        x = s2l(x)
        tempx = x[:]
        y = s2l(y)
        tempy = y[:]
    

if __name__ == '__main__':
    mx, my = Rho()
    print("the collision message :\nmx : {}\nmy : {}".format(mx, my))
    hashx = sm3.sm3_hash(mx)
    hashy = sm3.sm3_hash(my)
    print("hash(mx) : ", hashx)
    print("hash(my) : ", hashy)
    if (hashx[0:DLEN] == hashy[0:DLEN]):
        print("it is a true collision.")