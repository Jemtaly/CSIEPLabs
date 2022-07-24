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

经测试，加密 1 GB 文件耗时约 3.8 s.

![screenshot](/SM3/screenshots/sm3_test.png)
