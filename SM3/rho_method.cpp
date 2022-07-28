#include <stdio.h>
#include <string.h>
#include <time.h>
#include "sm3.hpp"
#define hash_size 4
struct hash_t {
	uint8_t data[hash_size];
	hash_t next() const {
		uint8_t buf[32];
		SM3().join_last(data, hash_size, buf);
		hash_t result;
		memcpy(result.data, buf, hash_size);
		return result;
	}
	bool operator==(hash_t const &rval) const {
		return !memcmp(data, rval.data, hash_size);
	}
};
/*
auto get_rho(const hash_t &seed) {
	hash_t x = seed, y = seed;
	do {
		x = x.next();
		y = y.next().next();
	} while (x != y);
	uint64_t rho = 0;
	do {
		x = x.next();
	} while (rho++, y != x);
	return rho;
}
*/
auto get_rho(hash_t const &seed) {
	hash_t x = seed;
	for (uint64_t n = 1;; n <<= 1) {
		hash_t y = x;
		for (uint64_t rho = 0; rho < n;) {
			x = x.next();
			if (rho++, x == y) {
				return rho;
			}
		}
	}
}
auto rho_method(hash_t const &seed) {
	uint64_t rho = get_rho(seed);
	hash_t x = seed, y = seed;
	for (uint64_t i = 0; i < rho; i++) {
		x = x.next();
	}
	for (;;) {
		auto x_tmp = x.next();
		auto y_tmp = y.next();
		if (x_tmp == y_tmp) {
			return std::pair<hash_t, hash_t>(x, y);
		}
		x = x_tmp;
		y = y_tmp;
	}
}
int main() {
	hash_t seed = {};
	printf("seed = ");
	print_digest(seed.data, hash_size);
	auto start = clock();
	auto res = rho_method(seed);
	auto end = clock();
	printf("Ma   = ");
	print_digest(res.first.data, hash_size);
	printf("Ha   = ");
	print_digest(res.first.next().data, hash_size);
	printf("Mb   = ");
	print_digest(res.second.data, hash_size);
	printf("Hb   = ");
	print_digest(res.second.next().data, hash_size);
	printf("time = %ld ms\n", end - start);
}
