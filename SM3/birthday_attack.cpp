#include <stdlib.h>
#include <iostream>
#include <unordered_map>
#include "sm3.hpp"
#define TIMES 100
#define hash_t uint32_t
auto birthday_attack(hash_t seed) {
	std::unordered_map<hash_t, hash_t> map;
	hash_t buf[32 / sizeof(hash_t)];
	for (hash_t i = seed;; i++) {
		SM3().join_last((uint8_t *)&i, sizeof(hash_t), (uint8_t *)buf);
		if (map.count(buf[0])) {
			return std::pair<hash_t, hash_t>(map[buf[0]], i);
		}
		map[buf[0]] = i;
	}
}
int main() {
	hash_t buf[32 / sizeof(hash_t)];
	int t = 0;
	for (int i = 0; i < TIMES; i++) {
		int seed = rand();
		printf("seed = %d:\n", seed);
		auto rec = clock();
		auto res = birthday_attack(seed);
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
