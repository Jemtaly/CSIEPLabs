#include <stdlib.h>
#include <iostream>
#include "sm3.hpp"
typedef uint64_t RT;
auto rho_method(RT start) {
	RT x, y;
	x = y = start;
	do {
		RT buf[32 / sizeof(RT)];
		SM3().join_last((uint8_t *)&x, sizeof(RT), (uint8_t *)buf);
		x = buf[0];
		SM3().join_last((uint8_t *)&y, sizeof(RT), (uint8_t *)buf);
		y = buf[0];
		SM3().join_last((uint8_t *)&y, sizeof(RT), (uint8_t *)buf);
		y = buf[0];
	} while (x != y);
	RT cycle = 0;
	do {
		RT buf[32 / sizeof(RT)];
		SM3().join_last((uint8_t *)&y, sizeof(RT), (uint8_t *)buf);
		y = buf[0];
		cycle++;
	} while (x != y);
	x = y = start;
	for (int i = 0; i < cycle; i++) {
		RT buf[32 / sizeof(RT)];
		SM3().join_last((uint8_t *)&x, sizeof(RT), (uint8_t *)buf);
		x = buf[0];
	}
	for (;;) {
		RT buf_x[32 / sizeof(RT)];
		RT buf_y[32 / sizeof(RT)];
		SM3().join_last((uint8_t *)&x, sizeof(RT), (uint8_t *)buf_x);
		SM3().join_last((uint8_t *)&y, sizeof(RT), (uint8_t *)buf_y);
		if (buf_x[0] == buf_y[0]) {
			return std::pair<RT, RT>(x, y);
		}
		x = buf_x[0];
		y = buf_y[0];
	}
}
int main() {
	RT buf[32 / sizeof(RT)];
	std::pair<RT, RT> res;
	do {
		res = rho_method(rand());
	} while (res.first == res.second);
	SM3().join_last((uint8_t *)&res.first, sizeof(RT), (uint8_t *)buf);
	printf("Ma = ");
	print_digest((uint8_t *)&res.first, sizeof(RT));
	printf("Ha = ");
	print_digest((uint8_t *)buf, sizeof(RT));
	SM3().join_last((uint8_t *)&res.second, sizeof(RT), (uint8_t *)buf);
	printf("Ma = ");
	print_digest((uint8_t *)&res.second, sizeof(RT));
	printf("Ha = ");
	print_digest((uint8_t *)buf, sizeof(RT));
}
