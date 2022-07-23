# include <stdint.h>
# include <stdio.h>
# include <stdlib.h>
# include <string.h>
# define SM3_DIGEST_LENGTH 32
# define SM3_WORD unsigned int

# define SM3_CBLOCK      64
# define SM3_LBLOCK      (SM3_CBLOCK/4)



#define ROTATE(a,n)     (((a)<<(n))|(((a)&0xffffffff)>>(32-(n))))

# define HOST_c2l32(c,l)  (l =(((unsigned long)(*((c)++)))<<24),          \
                           l|=(((unsigned long)(*((c)++)))<<16),          \
                           l|=(((unsigned long)(*((c)++)))<< 8),          \
                           l|=(((unsigned long)(*((c)++)))    )           )
# define HOST_l2c32(l,c)  (*((c)++)=(unsigned char)(((l)>>24)&0xff),      \
                           *((c)++)=(unsigned char)(((l)>>16)&0xff),      \
                           *((c)++)=(unsigned char)(((l)>> 8)&0xff),      \
                           *((c)++)=(unsigned char)(((l)    )&0xff))

# define HOST_c2l64(c,l)  (l =(((uint64_t)(*((c)++)))<<56),          \
                           l|=(((uint64_t)(*((c)++)))<<48),          \
                           l|=(((uint64_t)(*((c)++)))<<40),          \
                           l|=(((uint64_t)(*((c)++)))<<32),          \
                           l|=(((uint64_t)(*((c)++)))<<24),          \
                           l|=(((uint64_t)(*((c)++)))<<16),          \
                           l|=(((uint64_t)(*((c)++)))<< 8),          \
                           l|=(((uint64_t)(*((c)++)))<<  )           )
# define HOST_l2c64(l,c)  (*((c)++)=(unsigned char)(((l)>>56)&0xff),      \
                           *((c)++)=(unsigned char)(((l)>>48)&0xff),      \
                           *((c)++)=(unsigned char)(((l)>>40)&0xff),      \
                           *((c)++)=(unsigned char)(((l)>>32)&0xff),      \
                           *((c)++)=(unsigned char)(((l)>>24)&0xff),      \
                           *((c)++)=(unsigned char)(((l)>>16)&0xff),      \
                           *((c)++)=(unsigned char)(((l)>> 8)&0xff),      \
                           *((c)++)=(unsigned char)(((l)    )&0xff))

#define P0(X) (X ^ ROTATE(X, 9) ^ ROTATE(X, 17))
#define P1(X) (X ^ ROTATE(X, 15) ^ ROTATE(X, 23))

#define FF0(X,Y,Z) (X ^ Y ^ Z)
#define GG0(X,Y,Z) (X ^ Y ^ Z)

#define FF1(X,Y,Z) ((X & Y) | ((X | Y) & Z))
#define GG1(X,Y,Z) ((X & Y) | (~X & Z))

#define RND(A, B, C, D, E, F, G, H, TJ, Wi, Wj, FF, GG)           \
     do {                                                         \
       const SM3_WORD A12 = ROTATE(A, 12);                        \
       const SM3_WORD A12_SM = A12 + E + TJ;                      \
       const SM3_WORD SS1 = ROTATE(A12_SM, 7);                    \
       const SM3_WORD TT1 = FF(A, B, C) + D + (SS1 ^ A12) + (Wj); \
       const SM3_WORD TT2 = GG(E, F, G) + H + SS1 + Wi;           \
       D = C;                                                     \
       C = ROTATE(B, 9);                                          \
       B = A;                                                     \
       A = TT1;                                                   \
       H = G;                                                     \
       G = ROTATE(F, 19);                                         \
       F = E;                                                     \
       E = P0(TT2);                                               \
     } while(0)

#define EXPAND(W0,W7,W13,W3,W10) \
   (P1(W0 ^ W7 ^ ROTATE(W13, 15)) ^ ROTATE(W3, 7) ^ W10)

#define R1(A,B,C,D,E,F,G,H,TJ,Wi,Wj) \
   RND(A,B,C,D,E,F,G,H,TJ,Wi,Wj,FF0,GG0)

#define R2(A,B,C,D,E,F,G,H,TJ,Wi,Wj) \
   RND(A,B,C,D,E,F,G,H,TJ,Wi,Wj,FF1,GG1)

#define SM3_A 0x7380166fUL
#define SM3_B 0x4914b2b9UL
#define SM3_C 0x172442d7UL
#define SM3_D 0xda8a0600UL
#define SM3_E 0xa96f30bcUL
#define SM3_F 0x163138aaUL
#define SM3_G 0xe38dee4dUL
#define SM3_H 0xb0fb0e4eUL

#define T1 0x79cc4519
#define T2 0x7a879d8a
void padding(uint8_t *input, uint64_t len)
{
   int a = len / SM3_CBLOCK;
   int b = len % SM3_CBLOCK;
   len = 8 * len;
   input[a * SM3_CBLOCK + b] = 0x80;
   uint8_t *temp = (uint8_t *)malloc(8 * sizeof(uint8_t));
   HOST_l2c64(len, temp);
   temp -= 8;
   memset(&input[a * SM3_CBLOCK + b + 1], 0, SM3_CBLOCK - 9 - b);
   int j = 0;
   for (int i = (a + 1) * SM3_CBLOCK - 8; i < (a + 1) * SM3_CBLOCK; i++)
   {   
      input[i] = temp[j];
      j++; 
   }
}

void hash(uint8_t *input, uint8_t *output, size_t len)
{
   int n = len / SM3_CBLOCK + 1;
   SM3_WORD *W = (SM3_WORD *)malloc(68 * sizeof(SM3_WORD));
   uint32_t Wj_ = 0;
   SM3_WORD A, B, C, D, E, F, G, H;
   SM3_WORD V[8];
   A = SM3_A; B = SM3_B; C = SM3_C; D = SM3_D; E = SM3_E; F = SM3_F; G= SM3_G; H = SM3_H;
   for(int i = 0; i < n; i++){
      V[0] = A; V[1] = B; V[2] = C; V[3] = D; V[4] = E; V[5] = F; V[6] = G; V[7] = H;
      for (int j = 0; j < 16; j++)
         HOST_c2l32(input, W[j]);
      for (int j = 16; j < 68; j++)
         W[j] = EXPAND(W[j - 16], W[j - 9], W[j - 3], W[j - 13], W[j - 6]);
      for (int j = 0; j < 16; j++){
         Wj_ = W[j] ^ W[j + 4];
         R1(A, B, C, D, E, F, G, H, ROTATE(T1, j), W[j], Wj_);
         //printf("%x,%x,%x,%x,%x,%x,%x,%x\n", A, B, C, D, E, F, G, H);
      }
      for (int j = 16; j < 64; j++){
         Wj_ = W[j] ^ W[j + 4];
         R2(A, B, C, D, E, F, G, H, ROTATE(T2, j), W[j], Wj_);
         //printf("%x,%x,%x,%x,%x,%x,%x,%x\n", A, B, C, D, E, F, G, H);
      }
      A = V[0] ^ A; B = V[1] ^ B; C = V[2] ^ C; D = V[3] ^ D; E = V[4] ^ E; F = V[5] ^ F; G = V[6] ^ G; H = V[7] ^ H;
      //printf("%x,%x,%x,%x,%x,%x,%x,%x\n", A, B, C, D, E, F, G, H);
   }
   A = HOST_l2c32(A, output);
   B = HOST_l2c32(B, output);
   C = HOST_l2c32(C, output);
   D = HOST_l2c32(D, output);
   E = HOST_l2c32(E, output);
   F = HOST_l2c32(F, output);
   G = HOST_l2c32(G, output);
   H = HOST_l2c32(H, output);
}
int main()
{
   uint8_t message[512] = {0x61, 0x62, 0x63};
   uint8_t digest[512] = {0};
   uint64_t len = strlen((char*)message);
   printf("%d", strlen((char *)message));
   printf("\n");
   padding(message, len);
   for (int i = 0; i < 64; i++)
      printf("%x ", message[i]);
   hash(message, digest, len);
   for (int i = 0; i < 32; i++)
      printf("%x ", digest[i]);
}