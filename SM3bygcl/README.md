# SM3

## SM3生日攻击

files:
Project: implement the naïve birthday attack of reduced SM3

根据生日攻击的原理，当计算的hash值超过$2^{n/2}$就有$1/2$的概率找到碰撞，由于SM3的安全强度超过个人计算机的计算量，因此对SM3做了简化，只取计算出来的$DLEN * 4$位(如16位)，取随机数计算hash，测试找到碰撞的概率。其中SM3调用gmssl库中的sm3算法。

```
...
count: 5938
count: 5939
count: 5940
count: 5941
count: 5942
find the collision!
m0: 2022389587
m1: 2322670330
```

如上找到一个碰撞，16位的碰撞，大概用了6000次，在$[2^8,2^{16}]$中。
