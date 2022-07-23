# Bitcoin

## Project: forge a signature to pretend that you are Satoshi.

该项目实现了ECDSA签名和验证，并且实现了签名的伪造，其中签名的伪造只能得到某个特定hash值的签名，但是无法直接得到消息的签名值，随机选择$u,v$，计算$R'=(x',y')=uG+vP, r' = x' \pmod{n}$，为了通过验证，需要$s'^{-1}(e'G+r'P) = uG + vP$，令$e'=r'uv^{-1}\pmod{n},s'=r'v^{-1}\pmod{n}$，那么得到的$(r',s')$即为哈希值$e'$用未知的私钥$d$签的签名。

某次运行结果如下：
```
[9, 16]
75263518707598184987916378021939673586055614731957507592904438851787542395619
[13, 10]
SignVrfy pass
forge signature: hash(m') = 0, r' = 7, s' = 6
forged SignVrfy pass
```
