TARGET = proj
CC = avr-gcc
COPY = avr-objcopy
MCU = atmega328p

build: $(TARGET).hex

$(TARGET).hex: $(TARGET).elf
	$(COPY) -j .text -O ihex $(TARGET).elf $(TARGET).hex

$(TARGET).elf: $(TARGET).c
	$(CC) -mmcu=$(MCU) -Os -o $(TARGET).elf $(TARGET).c

# Programming with AVRDUDE
PROGRAMMER = avrispmkII
DEVICE = m328p
PORT = usb
AVRDUDE_FLAGS = -c $(PROGRAMMER) -p $(DEVICE) -P $(PORT)

prog:
	avrdude $(AVRDUDE_FLAGS) -U flash:w:$(TARGET).hex

sig:
	avrdude $(AVRDUDE_FLAGS)

