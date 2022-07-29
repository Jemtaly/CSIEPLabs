import sm2
import pysmx


def sm2_test():
    a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    P = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
    G = 0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7, 0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0
    print('a = 0x' + a.to_bytes(32, 'big').hex())
    print('b = 0x' + b.to_bytes(32, 'big').hex())
    print('p = 0x' + P.to_bytes(32, 'big').hex())
    print('n = 0x' + n.to_bytes(32, 'big').hex())
    print('G_x = 0x' + G[0].to_bytes(32, 'big').hex())
    print('G_y = 0x' + G[1].to_bytes(32, 'big').hex())
    sm2obj = sm2.SM2(32, a, b, P, n, G)
    print('d = 0x' + sm2obj.d.to_bytes(32, 'big').hex())
    print('P_x = 0x' + sm2obj.P[0].to_bytes(32, 'big').hex())
    print('P_y = 0x' + sm2obj.P[1].to_bytes(32, 'big').hex())
    M = b'abc'
    print('M = 0x' + M.hex())
    print('-------------------------- Encrypt and Decrypt --------------------------')
    C = sm2obj.encrypt(M)
    print('C = 0x' + C.hex())
    P = sm2obj.decrypt(C)
    print('P = 0x' + P.hex())
    print('Decryption succeeded.' if P == M else 'Decryption failed.')
    print('---------------------------- Sign and Verify ----------------------------')
    E = pysmx.SM3.digest(M)
    print('E = 0x' + E.hex())
    S = sm2obj.sign(E, rfc6979=True)
    print('S = 0x' + S.hex())
    print('Verification succeeded.' if sm2obj.verify(S, E) else 'Verification failed.')


if __name__ == '__main__':
    sm2_test()
