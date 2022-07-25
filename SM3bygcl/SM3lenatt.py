from gmssl import sm3
def padding(msg):# copied by gmssl
    len1 = len(msg)
    reserve1 = len1 % 64
    msg.append(0x80)
    reserve1 = reserve1 + 1
    # 56-64, add 64 byte
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end + 64

    for i in range(reserve1, range_end):
        msg.append(0x00)

    bit_length = (len1) * 8
    bit_length_str = [bit_length % 0x100]
    for i in range(7):
        bit_length = int(bit_length / 0x100)
        bit_length_str.append(bit_length % 0x100)
    for i in range(8):
        msg.append(bit_length_str[7-i])

    group_count = round(len(msg) / 64)

    B = []
    for i in range(0, group_count):
        B.append(msg[i*64:(i+1)*64])
    return B

def padding(msg):# copied by gmssl
    len1 = len(msg)
    reserve1 = len1 % 64
    msg.append(0x80)
    reserve1 = reserve1 + 1
    # 56-64, add 64 byte
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end + 64

    for i in range(reserve1, range_end):
        msg.append(0x00)

    bit_length = (len1) * 8
    bit_length_str = [bit_length % 0x100]
    for i in range(7):
        bit_length = int(bit_length / 0x100)
        bit_length_str.append(bit_length % 0x100)
    for i in range(8):
        msg.append(bit_length_str[7-i])

    group_count = round(len(msg) / 64)

    B = []
    for i in range(0, group_count):
        B.append(msg[i*64:(i+1)*64])
    return B

if __name__ == "__main__":
    x = [1,2,3]
    digest = sm3.sm3_hash(x)
    print("hash([1,2,3]):", digest)
    print("---length extension attack---")
    addmsg = [2,3,4]
    addmsgstur = addmsg[:]
    addmsgpad = padding(addmsg)
    Mlen = len(addmsgpad)
    tempp = "%0128s" %hex(sum(addmsgpad[-1][len(addmsgpad[-1]) - i - 1] * (256 ** i) for i in range(len(addmsgpad[-1]))) + 512 * Mlen)[2:]
    print(tempp)
    addmsgpad[-1] = [int(tempp[i:i + 2], base = 16) for i in range(0,128,2)]
    print(addmsgpad)
    temp = [int(digest[i:i + 8], base = 16) for i in range(0,64,8)]
    for i in range(len(addmsgpad)):
        digest1 = sm3.sm3_cf(temp, addmsgpad[i])
    result = ""
    for i in digest1:
        result = '%s%08x' % (result, i)
    print("hash([1,2,3]||padding||[2,3,4]):", result)
    xpad = padding(x)[0]
    print(xpad + addmsgstur)
    digest2 = sm3.sm3_hash(xpad + addmsgstur)
    print("the real hash:", digest2)
