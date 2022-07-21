#include <stdlib.h>
#include <iostream>
#include "sm3.hpp"
auto length_extension_attack(uint8_t *hash, uint64_t len) {
	SM3 sm3;
	for (int j = 0; j < 8; j++) {
		sm3.rec[j] = hash[j << 2] << 030 | hash[j << 2 | 1] << 020 | hash[j << 2 | 2] << 010 | hash[j << 2 | 3];
    }
	auto rem = len % 64;
	sm3.countr = (len - rem + (rem >= 56 ? 128 : 64)) * 8;
	return sm3;
}
int main() {
	SM3 sm3_a;
	uint8_t message_a[] =
		"ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ";
	uint8_t buf_a[32];
	sm3_a.join((uint8_t *)message_a);
	sm3_a.join_last((uint8_t *)message_a + 64, 40, buf_a);
	SM3 sm3_b = length_extension_attack(buf_a, 104);
	uint8_t message_b[] =
		"0123456789";
	uint8_t buf_b[32];
	sm3_b.join_last((uint8_t *)message_b, 10, buf_b);
	SM3 sm3_c;
	uint8_t message_c[] =
		"ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
		"\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x40"
		"0123456789";
	uint8_t buf_c[32];
	sm3_c.join((uint8_t *)message_c);
	sm3_c.join((uint8_t *)message_c + 64);
	sm3_c.join_last((uint8_t *)message_c + 128, 10, buf_c);
	printf("Ha =");
	for (int i = 0; i < 32; i++) {
		printf(" %02X", buf_a[i]);
	}
	printf("\n");
	printf("Hb =");
	for (int i = 0; i < 32; i++) {
		printf(" %02X", buf_b[i]);
	}
	printf("\n");
	printf("Hc =");
	for (int i = 0; i < 32; i++) {
		printf(" %02X", buf_c[i]);
	}
	printf("\n");
}
