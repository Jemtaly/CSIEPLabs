from gmssl import sm2, func
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
import hashlib
import random

private_key = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
public_key = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'

def generate_key():
    x = str(random.randint(0, 2 ** 32))
    m = hashlib.md5()
    m.update(x.encode("utf-8"))
    return m.hexdigest()[0 : 16]

if __name__ == "__main__":
    key = generate_key().encode()
    print("randomly generate the session key : ", key)
    iv = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    crysm4 = CryptSM4()
    crysm4.set_key(key, SM4_ENCRYPT)
    plaintext = 'fixedpoint'
    ciphertext = crysm4.crypt_ecb(plaintext.encode())
    sm2crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    enckey = sm2crypt.encrypt(key)
    print("----ENC----")
    print("SM2 enc key :", enckey)
    print("plaintext : ", plaintext)
    print("SM4 ciphertext : ", ciphertext)
    print("----DEC----")
    deckey = sm2crypt.decrypt(enckey)
    print("SM2 dec key : ", deckey.decode())
    crysm42 = CryptSM4()
    crysm42.set_key(deckey, SM4_DECRYPT)
    dectext = crysm42.crypt_ecb(ciphertext)
    print("SM4 dec ciphertext : ", dectext)

