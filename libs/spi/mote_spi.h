#ifndef _MOTE_SPI_H
#define _MOTE_SPI_H

//include the correct implementation for the chosen platform
#ifdef ARCH_AVR
        #include "AVR/mote_spi.c"
#endif
#ifdef ARCH_PIC
        #include "PIC/mote_spi.c"
#endif
#ifdef ARCH_ARM
        #include "ARM/mote_spi.c"
#endif

//available library functions
BYTE testme(BYTE input);


BOOL SendByte(DEVICE_ID to, BYTE input);
BYTE ReceiveByte(DEVICE_ID from);

BOOL SendWord(DEVICE_ID to, WORDinput);
WORD ReceiveWord(DEVICE_ID from);


BOOL SendCommand(DEVICE_ID to, COMMAND command);
COMMAND ReceiveCommand(DEVICE_ID from);

#endif