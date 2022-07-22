#include <stdlib.h>
#include <iostream>
#include "sm3.hpp"
struct data_t {
	size_t len;
	uint8_t *str;
};
void merkle_tree(data_t const *datalist, int start, int end, uint8_t *buf) {
	if (start == end) {
		uint8_t m[1025] = {0x00};
		memcpy((uint8_t *)m + 1, datalist[start].str, datalist[start].len);
		SM3_calc(m, datalist[start].len + 1, buf);
		printf("H%d   = ", start);
		print_digest(buf, 32);
	} else {
		int l = 1;
		while (start + l * 2 <= end) {
			l *= 2;
		}
		uint8_t m[65] = {0x01};
		merkle_tree(datalist, start, start + l - 1, (uint8_t *)m + 1);
		merkle_tree(datalist, start + l, end, (uint8_t *)m + 33);
		SM3_calc(m, 65, buf);
		printf("H%d~%d = ", start, end);
		print_digest(buf, 32);
	}
}
int main() {
	uint8_t a[] = "abcdefgh";
	uint8_t b[] = "ABCDEFGH";
	uint8_t c[] = "12345678";
	uint8_t d[] = "00000000";
	uint8_t e[] = "########";
	data_t datalist[5] = {
		{8, a},
		{8, b},
		{8, c},
		{8, d},
		{8, e},
	};
	uint8_t buf[32];
	merkle_tree(datalist, 0, 4, buf);
}
