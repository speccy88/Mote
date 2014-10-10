#include "avr/io.h"

void pinDirection(BYTE pin, BYTE dir) {
	if (pin==0 && dir==OUTPUT) DDRB |= (1<<B0);
	if (pin==0 && dir==INPUT)  DDRB &= ~(1<<B0);
}

void pinWrite(BYTE pin, BYTE state) {
	if (pin==0 && state==HIGH) PORTB |= (1<<B0);
	if (pin==0 && state==LOW)  PORTB &= ~(1<<B0);
}

BYTE pinRead(BYTE pin) {
}




