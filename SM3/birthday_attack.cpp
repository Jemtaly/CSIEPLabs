#include <stdlib.h>
#include <iostream>
#include <unordered_map>
#include "sm3.hpp"
typedef uint32_t RT;
auto birthday_attack() {
	std::unordered_map<RT, RT> map;
	RT i[64 / sizeof(RT)] = {};
	RT o[32 / sizeof(RT)] = {};
	for (i[0] = 0;; i[0]++) {
		SM3().join_last((uint8_t *)i, sizeof(RT), (uint8_t *)o);
		if (map.count(o[0])) {
			return std::pair<RT, RT>(map[o[0]], i[0]);
		}
		map[o[0]] = i[0];
	}
}
int main() {
	RT i[64 / sizeof(RT)] = {};
	RT o[32 / sizeof(RT)] = {};
	auto res = birthday_attack();
	i[0] = res.first;
	SM3().join_last((uint8_t *)i, sizeof(RT), (uint8_t *)o);
	printf("Ma = 0x%08X\n", i[0]);
	printf("Ha = 0x%08X\n", o[0]);
	i[0] = res.second;
	SM3().join_last((uint8_t *)i, sizeof(RT), (uint8_t *)o);
	printf("Mb = 0x%08X\n", i[0]);
	printf("Hb = 0x%08X\n", o[0]);
}
