# SM3

项目完成人：郭灿林

运行指导：需要第三方库gmssl，使用`pip install gmssl`进行安装，同时需要C语言和python编译环境

该文件夹主要存储SM3相关项目。
|文件名|对应项目|
|-|-|
|SM3biratt.py|Project:implement the naïve birthday attack of reduced SM3|
|SM3lenatt.py|Project:implement length extension attack for SM3|
|SM3Rho.py|Project:implement the Rho method of reduced SM3|
|SM3bygcl.c|Project:do your best to optimize SM3 implementation (software)|

## SM3生日攻击

files : SM3biratt.py

Project : implement the naïve birthday attack of reduced SM3

根据生日攻击的原理，当计算的hash值超过$2^{n/2}$就有$1/2$的概率找到碰撞，由于SM3的安全强度超过个人计算机的计算量，因此对SM3做了简化，只取计算出来的$DLEN * 4$位(如16位)，取随机数计算hash，测试找到碰撞的概率。其中SM3调用gmssl库中的sm3算法。

![pic](/SM3bygcl/ScreenShot/birthday.png)

如上找到一个碰撞，16位的碰撞，大概用了6000次，在$[2^8,2^{16}]$中。

## SM3长度扩展攻击

files : SM3lenatt.py

Project: implement length extension attack for SM3

由于gmssl里面没有单独padding的函数，所以我把gmssl的sm3中的`sm3_hash`函数里面的填充部分拿出来单独写成`padding`函数。

长度扩展攻击主要思路是任意计算一个hash值，将该hash值作为块更新函数`sm3_cf`的IV输入，消息块则输入要扩展的消息块，考虑输入多个消息块，这里用了一个for循环，需要注意的是，输入的消息块的最后一块需要加上原hash值消息块的长度，即该行代码后面的$512 * Mlen$，`tempp = "%0128s" %hex(sum(addmsgpad[-1][len(addmsgpad[-1]) - i - 1] * (256 ** i) for i in range(len(addmsgpad[-1]))) + 512 * Mlen)[2:]`。

```
    for i in range(len(addmsgpad)):
        digest1 = sm3.sm3_cf(temp, addmsgpad[i])
```

如图，`hash([1,2,3]||padding||[2,3,4]):`对应长度扩展攻击计算出来的hash值，`the real hash:`对应直接计算消息`[1,2,3]||padding||[2,3,4]`的hash值，可以看到两者是相等的，说明长度扩展攻击成功。

![pic](/SM3bygcl/ScreenShot/LengthExtension.png)

## SM3 Rho方法

files : SM3Rho.py

Project : implement the Rho method of reduced SM3

该项目参考了同组李岱耕的思路。

首先，随机生成一个数做hash后作为start起始点，然后用一个列表把计算过的hash存下来，迭代进行hash，每次都判断hash值是否在圈中出现，若出现则说明形成环，结束循环。（此处也可以用两个点进行迭代，一个快一个慢，比如$x = hash(x), y = hash(hash(y))$，若$x$和$y$出现碰撞，就说明形成环，该方法的好处则是用时间换空间，每次只需要存一个$x$和$y$，不需要把中间值存下，同样可以求得环的长度）

```
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
```

确定环的长度后，让x从start开始跑起，先跑循环的长度次，然后y再开始以同样的速度跑，这样x和y下次碰撞的时候就刚好是在x要进入环的时候，这时候产生的碰撞对应的消息值就是不同的了。

```
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
```

结果如图，本次运行的循环长度是254，找到如图的两个碰撞，重新hash可验证16位碰撞成功。

![pic](/SM3bygcl/ScreenShot/Rho.png)]
