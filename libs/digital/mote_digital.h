#ifndef _MOTE_DIGITAL_H
#define _MOTE_DIGITAL_H


//include the correct implementation for the chosen platform
#ifdef ARCH_AVR
	#include "AVR/mote_digital.c"
#endif
#ifdef ARCH_PIC
	#include "PIC/mote_digital.c"
#endif
#ifdef ARCH_ARM
	#include "ARM/mote_digital.c"
#endif


//available library functions
void pinDirection(BYTE pin, BYTE dir);
void pinWrite(BYTE pin, BYTE state);
BYTE pinRead(BYTE pin);

#endif
