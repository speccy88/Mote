#ifndef _PINS_H
#define _PINS_H

// AVR ATTiny25/45/85 8-DIP pin mapping

// Name the pins
// two bus lines for some kind of diferencial transmission, clock + data, etc.
// IO general ports could be used as a 4 pin sensor/actuator or as a 16 pin (multiplexed)

#define POWER_VCC	8 // just for information purposes
#define POWER_GND	4 // just for information purposes
#define BUS_A		1 // this pin could be locked for bus networking 
#define BUS_B		2 // also this one
#define IO_1		3 // general IO port #1 
#define IO_2		5 // ...
#define IO_3		6 // ...
#define IO_4		7 // ...


#endif