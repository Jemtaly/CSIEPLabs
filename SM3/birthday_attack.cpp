#include <stdlib.h>
#include <iostream>
#include <unordered_map>
#include "sm3.hpp"
typedef uint32_t RT;
auto birthday_attack() {
	std::unordered_map<RT, RT> map;
	RT buf[32 / sizeof(RT)];
	for (RT i = 0;; i++) {
		SM3().join_last((uint8_t *)&i, sizeof(RT), (uint8_t *)buf);
		if (map.count(buf[0])) {
			return std::pair<RT, RT>(map[buf[0]], i);
		}
		map[buf[0]] = i;
	}
}
int main() {
	RT buf[32 / sizeof(RT)];
	auto res = birthday_attack();
	SM3().join_last((uint8_t *)&res.first, sizeof(RT), (uint8_t *)buf);
	printf("Ma =");
	print_digest((uint8_t *)&res.first, sizeof(RT));
	printf("Ha =");
	print_digest((uint8_t *)buf, sizeof(RT));
	SM3().join_last((uint8_t *)&res.second, sizeof(RT), (uint8_t *)buf);
	printf("Ma =");
	print_digest((uint8_t *)&res.second, sizeof(RT));
	printf("Ha =");
	print_digest((uint8_t *)buf, sizeof(RT));
}
