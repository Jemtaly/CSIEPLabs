# SM3

项目完成人：郭灿林

运行指导：需要第三方库gmssl，使用`pip install gmssl`进行安装，同时需要C语言和python编译环境

该文件夹主要存储SM3相关项目。
|文件名|对应项目|
|-|-|
|SM3biratt.py|Project: implement the naïve birthday attack of reduced SM3|
|SM3lenatt.py|Project: implement length extension attack for SM3|
|SM3bygcl.c|Project: do your best to optimize SM3 implementation (software)|

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
