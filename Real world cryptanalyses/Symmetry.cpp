#include <stdint.h>
#include <stdio.h>
#include "meow_hash_x64_aesni.h"

uint64_t f(uint64_t x) {
    uint64_t symmetrize32[16] = {
        3224358602161482154llu, 1814594138510994814llu, 13954951486077169833llu, 12219675304746119337llu,
        32, 0, 0, 0,
        15245537510594700387llu, 11375056618140292268llu, 15015954861103735561llu, 7161769469951828835llu,
        0, 0, 0, 0
    };
    uint64_t message[4] = { x, x, x, x };
    meow_u128 h = MeowHash(symmetrize32, 32, message);
    return *(uint64_t*)&h;
}

void print_num(uint64_t x) {
    uint64_t* byte_ptr = &x;
    for (int i = 0; i < 8; i++)
        printf("%02x", byte_ptr[i]);
    printf("\n");
}

int main() {
    uint64_t tortoise = 0;
    uint64_t hare = 0;

    do {
        tortoise = f(tortoise);
        hare = f(f(hare));
    } while (tortoise != hare);
    printf("Cycle detected! Hare location: "); print_num(hare);

    uint64_t x1, x2;
    tortoise = 0;
    while (tortoise != hare) {
        x1 = tortoise;
        x2 = hare;
        tortoise = f(tortoise);
        hare = f(hare);
    }

    printf("Collision:\n");
    print_num(x1);
    print_num(x2);
}