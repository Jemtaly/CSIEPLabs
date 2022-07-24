# SM3

## Birthday Attack

针对 *32* 位简化 SM3 算法的生日攻击，在 O3 优化下耗时约 0.03 s, 最大内存占用量 4.7 MB.

![screenshot](/SM3/screenshots/birthday_attack.png)

## Rho Method

针对 *64* 位简化 SM3 算法的 Rho Method 攻击，经测试在 O3 优化下耗时约 3 h, 另外针对 *32* 位简化 SM3 算法耗时约为 0.04 s.

![screenshot](/SM3/screenshots/rho_method.png)

## Length Extension Attack

先计算出信息 `a = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"` 的 SM3 哈希值 `Ha`, 对齐进行长度扩展攻击，扩充一段信息 `b = "0123456789"` 并计算出新的哈希值 `Hb`, 然后与 `c = a || padding || b` 的哈希值 `Hc` 进行比较验证。

![screenshot](/SM3/screenshots/length_extension_attack.png)

## SM3 Optimization

经测试，优化后的算法加密 1 GB 文件耗时约 3.8 s.

![screenshot](/SM3/screenshots/sm3_test.png)

## Merkle Tree

依据协议 RFC6962 实现 Merkel 树，构造具有 10w 叶节点的 Merkle 树，可以对指定元素构建包含关系的证明，可以对指定元素构建不包含关系的证明。

思路：通过递归实现创建和遍历 Merkle 树，验证时先通过遍历查找元素对应的叶子节点，若未找到则证明不存在，否则一次验证其每个父节点是否正确，如果全部正确则证明存在，否则返回异常。

![screenshot](/SM3/screenshots/merkle_tree.png)
