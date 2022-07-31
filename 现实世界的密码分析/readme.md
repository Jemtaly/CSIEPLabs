# Real world cryptanalyses

贡献者：李婕

目录：

- [Encrypt](#Encrypt)

- [Invertibility](#Invertibility)

- [Symmetry](#Symmetry)


代码参考链接：https://peter.website/meow-hash-cryptanalysis

## Encrypt

### 根据上文链接测试加密结果如下：


针对 *32* 位简化 SM3 算法的生日攻击，在 O3 优化下单次攻击平均耗时约 30 ms, 最大内存占用量 4.7 MB.

![screenshot](screenshots/birthday_attack.png)

针对 *48* 位简化 SM3 算法的生日攻击，在 O3 优化下单次攻击耗时 12 s, 最大内存占用量 1.3 GB.

![screenshot](screenshots/birthday_attack_48.png)

针对 *64* 位简化 SM3 算法的生日攻击，在 O3 优化下单次攻击耗时间约 40 min, 最大内存占用量约 90 GB.

![screenshot](screenshots/birthday_attack_64.png)


## Invertibility

Mewo hash中所有部件均为可逆，且使用 1024 位密钥作为 1024 位初始状态，因此给定一个消息和目标哈希值，可以计算一个密钥。
只需将哈希函数的所有步骤从输出状态一直向后运行到初始状态。


### 算法说明


### squeeze_inverse函数如下：

该函数较为简单，只需按照正常步骤倒转即可，注意最后的通道变化。
    paddq(lanes[0], lanes[4])
    pxor(lanes[4], lanes[5])
    pxor(lanes[0], lanes[1])
    paddq(lanes[5], lanes[7])
    paddq(lanes[1], lanes[3])
    paddq(lanes[4], lanes[6])
    paddq(lanes[0], lanes[2])
    
### Finalization_inverse函数如下：

    pxor(lanes[0], lanes[1])
    paddq(lanes[4], lanes[5])
    aes_enc(lanes[3], lanes[0])
    pxor(lanes[3], lanes[5])
    paddq(lanes[0], lanes[4])
    pxor(lanes[3], lanes[5])
    aes_enc(lanes[7], lanes[3])
    
    
 ### 明文吸收函数如下：
 
 该部分较为复杂，输入的明文m长度是不可知的，因此将明文扩展成哈希所需的长度。
 
   将明文长度填充到32字节的倍数；若已经是一个倍数，则添加一个完整的零块
    original_length = len(input_bytes)
    target_length = ((len(input_bytes) // 32) + 1) * 32
    input_bytes += b"\0" * (target_length - original_length)

    剪掉最后一块
    input_bytes, tail_block = input_bytes[:-32], input_bytes[-32:]

    吸收所有256字节块
    off = 0
    while off + 256 <= len(input_bytes):
        for _ in range(8):
            meow_mix(0, input_bytes[off: off + 32])
            off += 32

    meow_mix_funky(0, tail_block)
    message_length_block = struct.pack("<QQQQ", 0, 0, original_length, 0)
    meow_mix_funky(1, message_length_block)

    while off + 32 <= len(input_bytes):
        meow_mix(2 + off // 32, input_bytes[off: off + 32])
        off += 32

    
 ### AES加密函数如下：
 
 正常哈希使用的是AES解密函数，获取密钥时应使用加密。
 
    def aes_enc(password: bytearray, text: bytearray):
    iv = b'1234567812345678'
    aes = AES.new(password, AES.MODE_CBC, iv)
    en_text = aes.encrypt(text)

### 测试结果

针对 *32* 位简化 SM3 算法的 Rho Method 攻击，经测试在 O3 优化下单次攻击耗时约 30 ms:

![screenshot](screenshots/rho_method.png)

针对 *64* 位简化 SM3 算法的 Rho Method 攻击，在 O3 优化下单次攻击耗时约 18 min:

![screenshot](screenshots/rho_method_64.png)

针对 *72* 位简化 SM3 算法的 Rho Method 攻击，在 O3 优化下单次攻击耗时约 13 h:

![screenshot](screenshots/rho_method_72.png)

## Symmetry



### 对称性内容说明

128 位值的高阶和低阶 64 位半部分相等，则将其称为对称值。Meow hash的三个操作：

在 128 位通道上应用一轮 AES 解密。
将 128 位值 Xor 转换为 128 位通道。
通过按元素添加低和高 64 位字，将 128 位值添加到 128 位通道中。

均具有对称性。巧妙利用“零长度消息”则可满足对称性。


### 运行结果


![screenshot](screenshots/sm3_test.png)



