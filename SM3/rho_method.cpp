#include <stdlib.h>
#include <iostream>
#include "sm3.hpp"
#define TIMES 100
#define hash_t uint32_t
auto get_rho(hash_t seed) {
	hash_t x = seed;
	for (hash_t n = 1;; n <<= 1) {
		hash_t y = x;
		for (hash_t rho = 0; rho < n;) {
			hash_t buf[32 / sizeof(hash_t)];
			SM3().join_last((uint8_t *)&x, sizeof(hash_t), (uint8_t *)buf);
			x = buf[0];
			if (rho++, x == y) {
				return rho;
			}
		}
	}
}
auto rho_method(hash_t seed) {
	hash_t rho = get_rho(seed);
	hash_t x = seed, y = seed;
	for (int i = 0; i < rho; i++) {
		hash_t buf[32 / sizeof(hash_t)];
		SM3().join_last((uint8_t *)&x, sizeof(hash_t), (uint8_t *)buf);
		x = buf[0];
	}
	for (;;) {
		hash_t buf_x[32 / sizeof(hash_t)];
		hash_t buf_y[32 / sizeof(hash_t)];
		SM3().join_last((uint8_t *)&x, sizeof(hash_t), (uint8_t *)buf_x);
		SM3().join_last((uint8_t *)&y, sizeof(hash_t), (uint8_t *)buf_y);
		if (buf_x[0] == buf_y[0]) {
			return std::pair<hash_t, hash_t>(x, y);
		}
		x = buf_x[0];
		y = buf_y[0];
	}
}
int main() {
	hash_t buf[32 / sizeof(hash_t)];
	int t = 0;
	for (int i = 0; i < TIMES; i++) {
		int seed = rand();
		printf("seed = %d:\n", seed);
		auto rec = clock();
		auto res = rho_method(seed);
		t += clock() - rec;
		SM3().join_last((uint8_t *)&res.first, sizeof(hash_t), (uint8_t *)buf);
		printf("Ma = ");
		print_digest((uint8_t *)&res.first, sizeof(hash_t));
		printf("Ha = ");
		print_digest((uint8_t *)buf, sizeof(hash_t));
		SM3().join_last((uint8_t *)&res.second, sizeof(hash_t), (uint8_t *)buf);
		printf("Mb = ");
		print_digest((uint8_t *)&res.second, sizeof(hash_t));
		printf("Hb = ");
		print_digest((uint8_t *)buf, sizeof(hash_t));
	}
	printf("average time = %d ms\n", t / TIMES);
}
