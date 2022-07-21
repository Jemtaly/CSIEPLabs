#include <stdlib.h>
#include <iostream>
#include "sm3.hpp"
typedef uint32_t RT;
auto rho_method(RT start) {
	RT x[64 / sizeof(RT)] = {};
	RT y[64 / sizeof(RT)] = {};
	x[0] = y[0] = start;
	do {
		RT buf[32 / sizeof(RT)];
		SM3().join_last((uint8_t *)x, sizeof(RT), (uint8_t *)buf);
		x[0] = buf[0];
		SM3().join_last((uint8_t *)y, sizeof(RT), (uint8_t *)buf);
		y[0] = buf[0];
		SM3().join_last((uint8_t *)y, sizeof(RT), (uint8_t *)buf);
		y[0] = buf[0];
	} while (x[0] != y[0]);
	RT cycle = 0;
	do {
		RT buf[32 / sizeof(RT)];
		SM3().join_last((uint8_t *)y, sizeof(RT), (uint8_t *)buf);
		y[0] = buf[0];
		cycle++;
	} while (x[0] != y[0]);
	x[0] = y[0] = start;
	for (int i = 0; i < cycle; i++) {
		RT buf[32 / sizeof(RT)];
		SM3().join_last((uint8_t *)x, sizeof(RT), (uint8_t *)buf);
		x[0] = buf[0];
	}
	for (;;) {
		RT buf_x[32 / sizeof(RT)];
		RT buf_y[32 / sizeof(RT)];
		SM3().join_last((uint8_t *)x, sizeof(RT), (uint8_t *)buf_x);
		SM3().join_last((uint8_t *)y, sizeof(RT), (uint8_t *)buf_y);
		if (buf_x[0] == buf_y[0]) {
			return std::pair<uint32_t, uint32_t>(x[0], y[0]);
		}
		x[0] = buf_x[0];
		y[0] = buf_y[0];
	}
}
int main() {
	RT i[64 / sizeof(RT)] = {};
	RT o[32 / sizeof(RT)] = {};
	std::pair<uint32_t, uint32_t> res;
	do {
		res = rho_method(rand());
	} while (res.first == res.second);
	i[0] = res.first;
	SM3().join_last((uint8_t *)i, sizeof(RT), (uint8_t *)o);
	printf("Ma = 0x%08X\n", i[0]);
	printf("Ha = 0x%08X\n", o[0]);
	i[0] = res.second;
	SM3().join_last((uint8_t *)i, sizeof(RT), (uint8_t *)o);
	printf("Mb = 0x%08X\n", i[0]);
	printf("Hb = 0x%08X\n", o[0]);
}
