#ifndef _NAMES_H
#define _NAMES_H


// *********************
// PIN NAMES
#ifdef ARCH_AVR
        #include "AVR/pins.h"
#endif

#ifdef ARCH_PIC
        #include "PIC/pins.h"
#endif

#ifdef ARCH_ARM
        #include "ARM/pins.h"
#endif



// *********************
// REG-FILE NAMES

// ...






#endif