from Crypto.Cipher import AES
import struct


def paddq(a: bytearray, b: bytearray):
    mask64 = 2 ** 64 - 1
    a0, a1 = struct.unpack("<QQ", a)
    b0, b1 = struct.unpack("<QQ", b)
    a[:] = struct.pack("<QQ", (a0 + b0) & mask64, (a1 + b1) & mask64)


def pxor(a: bytearray, b: bytearray):
    for i in range(16):
        a[i] ^= b[i]


def aes_enc(password: bytearray, text: bytearray):
    iv = b'1234567812345678'
    aes = AES.new(password, AES.MODE_CBC, iv)
    en_text = aes.encrypt(text)


def Final_ni(h1: bytes):
    lanes = [
        bytearray(h1[i * 16:16 + i * 16])
        for i in range(8)
    ]

    # squeeze_inverse:
    paddq(lanes[0], lanes[4])
    pxor(lanes[4], lanes[5])
    pxor(lanes[0], lanes[1])
    paddq(lanes[5], lanes[7])
    paddq(lanes[1], lanes[3])
    paddq(lanes[4], lanes[6])
    paddq(lanes[0], lanes[2])

    # Finalization_inverse

    pxor(lanes[0], lanes[1])
    paddq(lanes[4], lanes[5])
    aes_enc(lanes[3], lanes[0])
    pxor(lanes[3], lanes[5])
    paddq(lanes[0], lanes[4])
    pxor(lanes[3], lanes[5])
    aes_enc(lanes[7], lanes[3])

    return lanes


def meow_get_key(input_bytes: bytes, h1: bytes):
    lanes1 = Final_ni(h1)

    def meow_mix_reg(i, reads):
        lanes1 = Final_ni(h1)
        pxor(lanes1[0], lanes1[2])
        paddq(lanes1[1], reads[2])
        aes_enc(lanes1[3], lanes1[0])
        pxor(lanes1[3], reads[0])
        paddq(lanes1[5], reads[0])
        aes_enc(lanes1[7], lanes1[3])

    get_lane = lambda i: lanes1[i % 8]

    def meow_mix(i, block):
        meow_mix_reg(i, [
            block[offset: offset + 16] for offset in (15, 0, 1, 16)
        ])

    def meow_mix_funky(i, block):
        meow_mix_reg(i, (
            b"\0" + block[:15], block[:16], block[17:] + block[:1], block[16:],
        ))

    # 将明文长度填充到32字节的倍数；若已经是一个倍数，则添加一个完整的零块
    original_length = len(input_bytes)
    target_length = ((len(input_bytes) // 32) + 1) * 32
    input_bytes += b"\0" * (target_length - original_length)

    # 剪掉最后一块
    input_bytes, tail_block = input_bytes[:-32], input_bytes[-32:]

    # 吸收所有256字节块
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

    print(bytes(lanes1[0]).hex(), lanes1[1].hex())
    print(bytes(lanes1[2]).hex(), lanes1[3].hex())
    print(bytes(lanes1[4]).hex(), lanes1[5].hex())
    print(bytes(lanes1[6]).hex(), lanes1[7].hex())


# 消息值

m1 = "202020141138 lijie"
m = bytes(
    m1, encoding='utf-8')

# 哈希值为lane[0]，其余为随机设定值



h = bytes(
    ("sdu_cst_20220610"
     "Arbitrary value1."
     "Arbitrary value2."
     "Arbitrary value3."
     "Arbitrary value4."
     "Arbitrary value5."
     "Arbitrary value6."
     "Arbitrary value7."), encoding='utf-8')

print("消息为：",m1 )
print("哈希值为：sdu_cst_20220610")
print("求出的key的值为：")
meow_get_key(m, h)
