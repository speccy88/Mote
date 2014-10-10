//include the correct implementation for the chosen platform
#ifdef ARCH_AVR
        #include "AVR/mote_timing.c"
#endif
#ifdef ARCH_PIC
        #include "PIC/mote_timing.c"
#endif
#ifdef ARCH_ARM
        #include "ARM/mote_timing.c"
#endif

//available library functions
void usDelay(LONG us);
void msDelay(WORD ms);
void randomDelay(LONG us);



