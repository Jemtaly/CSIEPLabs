# SM2

项目完成人：郭灿林

|文件|项目|
|-|-|
||Project: verify the above pitfalls with proof-of-concept code|

## ECDSA的弱点



### Leaking $k$ leads to leaking of $d$

根据ECDSA的签名算法，有$s = k ^{-1}(e + dr) \pmod{n}$，可推得$d = (sk - e) ^ r^{-1} \pmod{n}$，若已知$k$，则可以直接得到$d$。

```

```

运行结果如下：

![pic](k2d.png)
