from random import *
from gmssl import sm3
DLEN = 4
def birthday():
    count = 0
    while(1):
        temp0 = randint(0, 2 ** 32)
        temp1 = randint(0, 2 ** 32)
        digest0 = sm3.sm3_hash([temp0])
        digest1 = sm3.sm3_hash([temp1])
        count = count + 1
        print("count:",count)
        if digest0[0:DLEN] == digest1[0:DLEN]:
            print("find the collision!")
            print("m0:",temp0)
            print("m1:",temp1)
            break

if __name__ == "__main__":
    birthday()
