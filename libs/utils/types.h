#ifndef _TYPES_H
#define _TYPES_H

//include the correct implementation for the chosen platform
#ifdef ARCH_AVR
    #include "AVR/types.c"
#endif
#ifdef ARCH_PIC
    #include "PIC/types.c"
#endif
#ifdef ARCH_ARM
    #include "ARM/types.c"
#endif


// **********************
// Some boolean values
#define FAIL	0
#define SUCCESS	1

#define FALSE	0
#define TRUE	1

#define LOW		0
#define HIGH	1

#define INPUT	0
#define OUTPUT	1


// **********************
// User defined types 
#define DEVICE_ID  WORD		// a unique number that identifies a mote or the MASTER
#define COMMAND    WORD 	// COMMANDS are unique numbers (up to 16 bit wide)




#endif
