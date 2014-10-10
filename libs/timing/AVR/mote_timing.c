#include "util/delay_basic.h"

void usDelay(LONG us) 
{
	// Here will go the code to make a 'us' microseconds delay
	
}

void msDelay(WORD ms) {
	int i;
	for(i=0;i<ms;i++) _delay_loop_2(300);
}

void randomDelay(LONG us) 
{
	// Here will go the code to make a random delay up to 'us' microseconds.
	
}
