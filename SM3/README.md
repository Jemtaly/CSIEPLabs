# SM3

## Birthday Attack

### 编译和运行

在此目录下执行以下命令：

```
g++ birthday_attack.cpp -std=c++20 -o birthday_attack.exe -O3
./birthday_attack.exe
```

### 测试结果

针对 *32* 位简化 SM3 算法的生日攻击，在 O3 优化下单次攻击平均耗时约 24 ms, 最大内存占用量 4.7 MB.

![screenshot](/SM3/screenshots/birthday_attack.png)

## Rho Method

### 编译和运行

在此目录下执行以下命令：

```
g++ rho_method.cpp -std=c++20 -o rho_method.exe -O3
./rho_method.exe
```

注：将 rho_method.cpp 中 hash_t 的定义修改为 uint64_t，并适当减小 TIMES 的数值，即可测试针对 *64* 位简化 SM3 算法的 Rho Method 攻击。

### 测试结果

针对 *32* 位简化 SM3 算法的 Rho Method 攻击，经测试在 O3 优化下单次攻击平均耗时约 51 ms:

![screenshot](/SM3/screenshots/rho_method.png)

另外针对 *64* 位简化 SM3 算法也进行了测试，耗时约为 30 min.

![screenshot](/SM3/screenshots/rho_method_64.png)

## Length Extension Attack

### 编译和运行

在此目录下执行以下命令：

```
g++ length_extension_attack.cpp -std=c++20 -o length_extension_attack.exe -O3
./length_extension_attack.exe
```

### 测试内容说明

先通过 SM3 算法计算出信息 `a = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"` 对应的哈希值 `Ha`, 对其进行长度扩展攻击，扩充一段信息 `b = "0123456789"` 并计算出新的哈希值 `Hb`, 然后与直接计算 `c = a || padding || b` 得到的哈希值 `Hc` 进行比较验证。

![screenshot](/SM3/screenshots/length_extension_attack.png)

## SM3 Optimization

### 编译和运行

在此目录下执行以下命令：

```
g++ sm3_test.cpp -std=c++20 -o sm3_test.exe -O3
./sm3_test.exe
```

### 测试结果

经测试，优化后的算法加密 1 GB 文件耗时约 3.8 s.

![screenshot](/SM3/screenshots/sm3_test.png)

## Merkle Tree

### 项目要求

依据协议 RFC6962 实现 Merkel 树，构造具有 10w 叶节点的 Merkle 树，可以对指定元素构建包含关系的证明，可以对指定元素构建不包含关系的证明。


### 编译和运行

在此目录下执行以下命令：

```
g++ merkle_tree.cpp -std=c++20 -o merkle_tree.exe -O3
./merkle_tree.exe
```

### 思路

创建 MerkleTree 类，通过递归实现其创建和遍历，验证某一元素是否存在时时先通过遍历找到其对应的叶子节点，若未找到则证明不存在，否则依次验证该叶子节点每个父节点是否正确，如果全部正确则证明存在，否则返回异常。

### 测试结果

![screenshot](/SM3/screenshots/merkle_tree.png)
