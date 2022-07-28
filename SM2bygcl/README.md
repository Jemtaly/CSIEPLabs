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

### Two users, using $k$ leads to leaking of $d$, that is they can deduce each other’s $d$

若两个用户使用同样的$k$加密签名，那么有$r = r_1 = r_2, s_1=k^{-1}(e_1+d_1r),s_2=k^{-1}(e_2+d_1r) $，即$ks_1=(e_1+d_1r),ks_2=(e_2+d_2r)$，两式相除可得$s_1/s_2=(e_1+d_1r)/(e_2+d_2r)$，若对于用户2已知$d_2$，则可得$d_1 = (s_1(e_2+d_2r)/s_2 - e_1)/r$，同理也可由$d_1$求得$d_2$。

```
def same_k_d22d1(k, G, P, n, d2, e1, e2, r1, r2, s1, s2):
    r = r1
    d2 = (s1*(e2+d2*r)*inverse(s2,n)-e1)*inverse(r,n)
    return d2
```

### Malleability of ECDSA, e.g. $(r,s)$ and $(r,-s)$ are both valid signatures, lead to blockchain network split

对于$(r,s)$验签，计算$es^{-1}G+rs^{-1}P=(x',y')$，若$r = x'$则通过验证；对于$(r,-s)$，计算
$e(-s)^{-1}G+r(-s)^{-1}P=-(es^{-1}G+rs^{-1}P)=(x',-y')$，得到的点的横坐标同样是$x'$，可通过验证。
```

```

### Ambiguity of DER encode could lead to blockchain network split



### One can forge signature if the verification does not check $m$

这部分和Project : forge a signature to pretend that you are Satoshi差不多在此不做赘述，可见`/Projects/Bitcoin/`文件夹。

### Same $d$ and $k$, used in ECDSA & Schnorr signature, leads to leaking of $d$

