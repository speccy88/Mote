#define ARCH_AVR

#include "../libs/platform.h"

int main(void) {
	pinDirection(0, OUTPUT);
	while(1) {
		msDelay(1000);
		pinWrite(0, HIGH);
		msDelay(2000);
		pinWrite(0, LOW);
	}
	return 0;
}
