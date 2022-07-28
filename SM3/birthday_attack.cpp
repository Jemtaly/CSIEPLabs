#include "sm3.hpp"
#include <stdio.h>
#include <string.h>
#include <unordered_map>
#define hash_size 6 // 取值不能大于 8
auto hash(uint64_t data) {
	uint64_t buf[4];
	SM3().join_last((uint8_t *)&data, hash_size, (uint8_t *)buf);
	return buf[0] & (1ull << 8 * hash_size) - 1;
}
auto birthday_attack(uint64_t seed) {
	std::unordered_map<uint64_t, uint64_t> map;
	for (uint64_t i = seed;; i++) {
		auto n = hash(i);
		if (map.count(n)) {
			return std::pair<uint64_t, uint64_t>(map[n], i);
		}
		map[n] = i;
	}
}
int main() {
	uint64_t buf[4];
	uint64_t seed = 0;
	printf("seed = ");
	print_digest((uint8_t *)&seed, hash_size);
	auto start = clock();
	auto res = birthday_attack(seed);
	auto end = clock();
	SM3().join_last((uint8_t *)&res.first, hash_size, (uint8_t *)buf);
	printf("Ma   = ");
	print_digest((uint8_t *)&res.first, hash_size);
	printf("Ha   = ");
	print_digest((uint8_t *)buf, hash_size);
	SM3().join_last((uint8_t *)&res.second, hash_size, (uint8_t *)buf);
	printf("Mb   = ");
	print_digest((uint8_t *)&res.second, hash_size);
	printf("Hb   = ");
	print_digest((uint8_t *)buf, hash_size);
	printf("time = %ld ms\n", end - start);
}
