#include <stdlib.h>
#include <iostream>
#include "sm3.hpp"
auto length_extension_attack(uint8_t *hash, uint64_t len) {
	SM3 sm3;
	for (int j = 0; j < 8; j++) {
		sm3.rec[j] = hash[j << 2] << 030 | hash[j << 2 | 1] << 020 | hash[j << 2 | 2] << 010 | hash[j << 2 | 3];
	}
	sm3.countr = len / 64 * 512 + (len % 64 >= 56 ? 1024 : 512);
	return sm3;
}
int main() {
	uint8_t buf_a[32];
	SM3_calc(
		(uint8_t *)"ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ",
		104, buf_a);
	uint8_t buf_b[32];
	SM3_calc(
		(uint8_t *)"0123456789",
		10, buf_b, length_extension_attack(buf_a, 104));
	uint8_t buf_c[32];
	SM3_calc(
		(uint8_t *)
			"ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
			"\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x40"
			"0123456789",
		138, buf_c);
	printf("Ha =");
	print_digest(buf_a, 32);
	printf("Hb =");
	print_digest(buf_b, 32);
	printf("Hc =");
	print_digest(buf_c, 32);
}
