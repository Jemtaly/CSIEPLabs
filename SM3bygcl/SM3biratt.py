from SM3FromInter import *
from random import *

DLEN = 4
def birthday():
    count = 0
    while(1):
        m0 = Fill(str(randint(0, 2 ** 32)))
        m1 = Fill(str(randint(0, 2 ** 32)))
        M0 = Group(m0)
        M1 = Group(m1)
        Vn0 = Iterate(M0)
        Vn1 = Iterate(M1)
        result0 = ''
        result1 = ''
        for x in Vn0:
            result0 += hex(x)[2:]
        for x in Vn1:
            result1 += hex(x)[2:]
        count = count + 1
        print("count:",count)
        if result0[0:DLEN] == result1[0:DLEN]:
            print("find the collision!")
            print("m0:",m0)
            print("m1:",m1)
            break

if __name__ == "__main__":
    birthday()
