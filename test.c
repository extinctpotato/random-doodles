#include <stdio.h>
#include <linux/time.h>

int main(int argc, char **argv) {
	printf("Hello world %d\n", argc);

	for (int i=0; i < argc; i++) {
		printf("argv[%d]: %s\n", i, argv[i]);
	}

	printf("%lu, %lu, %lu\n", 
			sizeof(long long int), 
			sizeof(int), 
			sizeof(struct timeval)
			);
}
