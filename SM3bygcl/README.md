# SM3

## SM3生日攻击

Project: implement the naïve birthday attack of reduced SM3

根据生日攻击的原理，当计算的hash值超过$2^{n/2}$就有$1/2$的概率找到碰撞，由于SM3的安全强度超过个人计算机的计算量，因此对SM3做了简化，只取计算出来的$DLEN * 4$位(如16位)，取随机数计算hash，测试找到碰撞的概率。

```
...
count: 53624
count: 53625
count: 53626
count: 53627
count: 53628
find the collision!
m0: 3772778161
m1: 3618364608
```

如上找到一个碰撞，16位的碰撞，大概用了50000次，在$[2^8,2^{16}]$中。
