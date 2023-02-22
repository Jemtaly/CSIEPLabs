# SM3

项目完成人：郭灿林

运行指导：需要第三方库 gmssl，使用 `pip install gmssl` 进行安装，同时需要 C 语言和 python 编译环境

该文件夹主要存储 SM3 相关项目。

| 文件名 | 对应项目 |
| --- | --- |
| SM3biratt.py | Project:implement the naïve birthday attack of reduced SM3 |
| SM3lenatt.py | Project:implement length extension attack for SM3 |
| SM3Rho.py | Project:implement the Rho method of reduced SM3 |
| SM3bygcl.c | Project:do your best to optimize SM3 implementation (software) |

## SM3 生日攻击

file: SM3biratt.py

Project: implement the naïve birthday attack of reduced SM3

根据生日攻击的原理，当计算的 hash 值超过 $2^{n/2}$ 就有 $1/2$ 的概率找到碰撞，由于 SM3 的安全强度超过个人计算机的计算量，因此对 SM3 做了简化，只取计算出来的 $DLEN*4$ 位 (如 16 位)，取随机数计算 hash，每次计算完检验一下列表中是否有该 hash 值，若有，则找到碰撞，否则，存入列表中。其中 SM3 调用 gmssl 库中的 sm3 算法。

如下图，找到一个 32 位的碰撞，计算了 36671 次 hash。

![pic](/SM3bygcl/ScreenShot/birthday.png)

下图为 48 位的碰撞，计算了 13413973 次 hash。

![pic](/SM3bygcl/ScreenShot/birthday48.png)

## SM3 长度扩展攻击

file: SM3lenatt.py

Project: implement length extension attack for SM3

由于 gmssl 里面没有单独 padding 的函数，所以我把 gmssl 的 sm3 中的 `sm3_hash` 函数里面的填充部分拿出来单独写成 `padding` 函数。

长度扩展攻击主要思路是任意计算一个 hash 值，将该 hash 值作为块更新函数 `sm3_cf` 的 IV 输入，消息块则输入要扩展的消息块，考虑输入多个消息块，这里用了一个 for 循环，需要注意的是，输入的消息块的最后一块需要加上原 hash 值消息块的长度，即该行代码后面的 $512*Mlen$，`tempp = "%0128s" %hex(sum(addmsgpad[-1][len(addmsgpad[-1]) - i - 1] * (256 ** i) for i in range(len(addmsgpad[-1]))) + 512 * Mlen)[2:]`。

```
    for i in range(len(addmsgpad)):
        digest1 = sm3.sm3_cf(temp, addmsgpad[i])
```

如图，`hash([1,2,3] || padding || [2,3,4]):` 对应长度扩展攻击计算出来的hash值，`the real hash:` 对应直接计算消息 `[1,2,3] || padding || [2,3,4]` 的 hash 值，可以看到两者是相等的，说明长度扩展攻击成功。

![pic](/SM3bygcl/ScreenShot/LengthExtension.png)

## SM3 Rho 方法

file: SM3Rho.py

Project: implement the Rho method of reduced SM3

Rho 方法相对于生日攻击来说，是利用时间换空间，可以用两个点进行迭代，一个快一个慢，比如 $x = hash (x), y = hash (hash (y))$，根据 Floyd 环的原理，$x$ 和 $y$ 一定会相遇，若 $x$ 和 $y$ 出现碰撞，就说明形成环，该方法每次只需要存一个 $x$ 和 $y$，不需要把中间值存下，同样可以求得环的长度。

```
    start = sm3.sm3_hash([randint(0, 2 ** 32)])
    x = s2l(start)[:]
    y = s2l(start)[:]
    l = 0
    while(1):
        x = sm3.sm3_hash(x)
        tempx = x[:]
        x = s2l(x)[0:DLEN]
        y = sm3.sm3_hash(y)
        y = s2l(y)[0:DLEN]
        y = sm3.sm3_hash(y)
        tempy = y[:]
        y = s2l(y)[0:DLEN]
        # print(tempx)
        # print(tempy)
        # print(l)
        if (tempx[0:DLEN] == tempy[0:DLEN]):
            break
    endx = x[:]
    while(1):
        l = l + 1
        x = sm3.sm3_hash(x)
        x = s2l(x)[0:DLEN]
        if (x == endx[0:DLEN]):
            break
```

确定环的长度后，让 x 从 start 开始跑起，先跑循环的长度次，然后 y 再开始以同样的速度跑，这样 x 和 y 下次碰撞的时候就刚好是在 x 要进入环的时候，这时候产生的碰撞对应的消息值就是不同的了。

```
    x = s2l(start)[:]
    y = s2l(start)[:]
    for i in range(l):
        x = sm3.sm3_hash(x)
        x = s2l(x)[0:DLEN]
    #print(x)
    while(1):
        x = sm3.sm3_hash(x)
        y = sm3.sm3_hash(y)
        if(x[0:DLEN] == y[0:DLEN]):
            return [tempx, tempy]
        x = s2l(x)[0:DLEN]
        tempx = x[:]
        y = s2l(y)[0:DLEN]
        tempy = y[:]
```

结果如图，本次运行的循环长度是 19580，找到如图的两个碰撞，重新 hash 可验证 32 位碰撞成功。

![pic](/SM3bygcl/ScreenShot/Rho.png)

下图为 48 位碰撞成功，循环长度为 1578466。

![pic](/SM3bygcl/ScreenShot/Rho48.png)

## SM3 实现和优化

file: SM3bygcl.c

Project: do your best to optimize SM3 implementation (software)

用 C 语言实现了 SM3，计算结果如下：

![pic](./ScreenShot/SM3_result.png)
