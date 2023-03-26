#include <stdio.h>
#include <unistd.h>
#include <termios.h>
#include <string.h>

int main(int argc, char **argv) {
	struct termios s;
	int fd = 0;
	int maxlen = 3;
	char buf[3];

	// Populate the struct and handle errors
	if (tcgetattr(fd, &s) < 0) {
		dprintf(2, "Error reading terminal settings\n");
	}

	s.c_lflag &= ~(ECHO | ICANON); // set cflags typical for the cbreak mode
	s.c_cc[VMIN] = maxlen;         // set minimum chars count to max sequence length
	s.c_cc[VTIME] = 1;             // time out after 1/10 of a second

	if (tcsetattr(fd, TCSAFLUSH, &s) < 0) {
		dprintf(2, "Error setting terminal settings\n");
	}

	int len = read(fd, buf, maxlen);
	printf("Read %d characters\n", len);

	for (int i = 0; i < strlen(buf); i++) {
		printf("[%d] %d\n", i, buf[i]);
	}
}
