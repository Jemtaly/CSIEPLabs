#include <stdlib.h>
#include <iostream>
#include "sm3.hpp"
#define BUFSIZE 4096
int main(int argc, char **argv) {
	for (int i = 1; i < argc; i++) {
		FILE *fp = fopen(argv[i], "rb");
		if (fp == nullptr) {
			printf("Cannot open %s!", argv[i]);
		}
		SM3 sm3;
		uint8_t readbuf[BUFSIZE], hashbuf[32];
		size_t len = fread(readbuf, 1, BUFSIZE, fp);
		while (len == BUFSIZE) {
			for (size_t j = 0; j < BUFSIZE; j += 64) {
				sm3.join(readbuf + j);
			}
			len = fread(readbuf, 1, BUFSIZE, fp);
		}
		size_t n = len - len % 64;
		for (size_t j = 0; j < n; j += 64) {
			sm3.join(readbuf + j);
		}
		sm3.join_last(readbuf + n, len % 64, hashbuf);
		printf("%s: ", argv[i]);
		print_digest(hashbuf, 32);
	}
}
