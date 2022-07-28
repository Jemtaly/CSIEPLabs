#include "sm3.hpp"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
struct data_t {
	size_t len;
	uint8_t *str;
};
class MerkleTree {
	size_t count;
	MerkleTree *left;
	MerkleTree *right;
	uint8_t hash[32];
	bool check_inner(uint8_t *h, size_t start) {
		if (count == 1) {
			if (memcmp(hash, h, 32)) {
				return false;
			}
		} else {
			if (left->check_inner(h, start)) {
				printf("H[%5llu, %5llu] = ", start + left->count, start + count - 1);
				print_digest(right->hash, 32);
			} else if (right->check_inner(h, start + left->count)) {
				printf("H[%5llu, %5llu] = ", start, start + left->count - 1);
				print_digest(left->hash, 32);
			} else {
				return false;
			}
			uint8_t m[65], buf[32];
			m[0] = 0x01;
			memcpy(m + 1, left->hash, 32);
			memcpy(m + 33, right->hash, 32);
			SM3_calc(m, 65, buf);
			if (memcmp(hash, buf, 32)) {
				throw std::exception();
			}
		}
		printf("H[%5llu, %5llu] = ", start, start + count - 1);
		print_digest(hash, 32);
		return true;
	}
public:
	MerkleTree(data_t const *datalist, size_t c): count(c), left(nullptr), right(nullptr) {
		if (count == 1) {
			uint8_t m[datalist->len + 1];
			m[0] = 0x00;
			memcpy(m + 1, datalist->str, datalist->len);
			SM3_calc(m, datalist->len + 1, hash);
		} else {
			size_t l = 1;
			while (l * 2 < count) {
				l *= 2;
			}
			left = new MerkleTree(datalist, l);
			right = new MerkleTree(datalist + l, count - l);
			uint8_t m[65];
			m[0] = 0x01;
			memcpy(m + 1, left->hash, 32);
			memcpy(m + 33, right->hash, 32);
			SM3_calc(m, 65, hash);
		}
	}
	void check(data_t data) {
		uint8_t m[data.len + 1], buf[32];
		m[0] = 0x00;
		memcpy(m + 1, data.str, data.len);
		SM3_calc(m, data.len + 1, buf);
		try {
			printf(check_inner(buf, 0) ? "The element is in the tree.\n" : "The element is not in the tree.\n");
		} catch (...) {
			printf("Error!\n");
		}
	}
	~MerkleTree() {
		if (count > 1) {
			delete left;
			delete right;
		}
	}
};
int main() {
	uint32_t seed = 1;
	data_t *datalist = (data_t *)calloc(100001, sizeof(data_t));
	for (size_t i = 0; i < 100001; i++) {
		datalist[i].len = 4;
		datalist[i].str = (uint8_t *)malloc(4);
		*(uint32_t *)datalist[i].str = seed;
		seed = (seed * 16807 + 1) % 0xffffffff;
	}
	MerkleTree mt(datalist, 100000);
	printf("------------------------------------------------ Inclusion Proof ------------------------------------------------\n");
	mt.check(datalist[12345]);
	printf("------------------------------------------------ Exclusion Proof ------------------------------------------------\n");
	mt.check(datalist[100000]);
	for (size_t i = 0; i < 100001; i++) {
		free(datalist[i].str);
	}
	free(datalist);
}
