# SM2

项目完成人：郭灿林

|文件|项目|
|-|-|
||Project: verify the above pitfalls with proof-of-concept code|

## ECDSA的弱点



### Leaking $k$ leads to leaking of $d$

根据ECDSA的签名算法，有$s = k^{-1}(e + dr) \pmod{n}$，可推得$d = (sk - e)  r^{-1} \pmod{n}$，若已知$k$，则可以直接得到$d$。

```
def k2d(k, G, P, n, e, r, s):
    d = ((s * k - e) * inverse(r, n)) % n
    return d
```

运行结果如下：

![pic](k2d.png)

### Reusing $k$ leads to leaking of $d$

若两次签名$(r_1,s_1)$和$(r_2,s_2)$使用同一个$k$，那么有$r = r_1 = r_2$,$s_1=k^{-1}(e_1+dr),s_2=k^{-1}(e_2+dr)$，即$ks_1=(e_1+dr),ks_2=(e_2+dr)$，两式相除可得$s_1/s_2=(e_1+dr)/(e_2+dr)$，整理可得$s_1e_2/s_2 +s_1dr/s_2 = e_1 + dr, d= (e_1-s_1e_2/s_2)/(s_1r/s_2-r),d = (e_1s_2-s_1e_2)/(s_1r-rs_2)$ 。

```
def rek2d(k1, k2, G, P, n, e1, e2, r1, r2, s1, s2):
    r = r1
    d = ((e1 * s2 - s1 * e2) * inverse(s1 * r - r * s2, n))  % n
    return d
```

###
