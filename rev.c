#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

int main(int argc, char **argv) {
	char buf[128];
	int offset = 0;
	int fd = 0;

	if (argc == 2) {
		fd = open(argv[1], O_RDONLY);

		if (fd == -1) {
			dprintf(2, "Error opening %s: %s\n", argv[1], strerror(errno));
		}
	}

	while(read(fd, buf+offset, 1) > 0) {
		if (buf[offset] == '\n') {
			for (int i = offset - 1; i >= 0; i--) {
				printf("%c", buf[i]);
			}
			printf("\n");
			memset(buf, 0, sizeof buf);
			offset = 0;	
		} else {
			offset++;
		}
	}

	close(fd);
}
