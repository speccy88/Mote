import RPi.GPIO as GPIO
from time import sleep
import serial

BAUDRATE = 9600
ser = None

# BCM to WiringPi pin numbers
P0 = 17 # not used
P1 = 18 # not used
P2 = 27 # not used - only for rev 2 pi
P3 = 22 # not used
P4 = 23 # not used
P5 = 24 # not used
p6 = 25 # rx enable 
p7 = 4  # tx enable

def Init():
    GPIO.setwarnings(False) # suppress GPIO used message
    GPIO.setmode(GPIO.BCM) # use BCM pin numbers
    GPIO.setup(p6, GPIO.OUT)
    GPIO.setup(p7, GPIO.OUT)
    #Setup serial port
    DisableTX() #don't send to garbage on the bus
    DisableRX()
    global ser
    ser = serial.Serial("/dev/ttyAMA0",BAUDRATE)
    ser.flush()

def EnableRX():
    GPIO.output(p6, GPIO.LOW)
    sleep(0.1)

def DisableRX():
    GPIO.output(p6, GPIO.HIGH)

def EnableTX():
    GPIO.output(p7, GPIO.HIGH)
    sleep(0.1)

def DisableTX():
    sleep(0.1) #wait 100ms before disable
    #to prevent disabling before sending
    GPIO.output(p7, GPIO.LOW)

def SendMSG(dst, src="A", data=""):
    NUL = chr(0)
    LEN = len(data)
    if LEN > 99:
        raise Exception("data cannot be more than 99")
    msg = [NUL] #Preamble
    msg.append(dst) #Destination
    msg.append(src) #Source, RPi is first device (always A)
    lenStr = format(LEN, "02d") #Length must be a string
    msg.append(lenStr[0]) #ten
    msg.append(lenStr[1]) #unit
    msg = msg + list("".join(data)) #append data
    checkSum = 0 #compute checksum
    for char in msg[1:]:
        num = ord(char) #char to decimal
        checkSum+=num
    checkSum = checkSum & 0xFF #Keep under 256
    msg.append(chr(checkSum)) #Back to ASCII
    payload = "".join(msg) #List to string
    EnableTX()
    ser.write(payload) #send the string
    DisableTX()

def Poll(dst):
    SendMSG(dst)
    recv = ReadMSG()

    CMD_OFFSET = 4
    if len(recv) == 4: #idle packet
        print "IDLE"
    elif recv[CMD_OFFSET] == "!": #Store
        print "STORE"
        StoreHandle(recv)
    elif recv[CMD_OFFSET] == "@": #Fetch
        print "FETCH"
        FetchHandle(dst, recv)
    else:
        print "POLLED RESPONSE FAILED"

    print recv

def Store(dst, topic):
    SendMSG(dst, data="!"+topic) 

def Fetch(dst, topic):
    SendMSG(dst, data="@"+topic)
    recv = ReadMSG()
    return recv

def ReadMSG():
    EnableRX()
    NUL = chr(0)
    HEADER_LEN = 4
    OFFSET_LEN = 3
    char = NUL
    #Wait for beginning of data
    while char == NUL:
        char = ser.read(1)
    header = char + ser.read(HEADER_LEN-1)
    lenStr = header[OFFSET_LEN:HEADER_LEN+1]
    DATA_LEN = int(lenStr)
    data = ser.read(DATA_LEN+1) #include checksum
    payload = header+data
    checkSum = 0 #compute checksum
    for char in payload[:-1]:
        num = ord(char) #char to decimal
        checkSum+=num
    checkSum = checkSum & 0xFF #Keep under 256
    if checkSum != ord(payload[-1]):
        raise Exception("Checksum error in ReadMSG")
    DisableRX()
    return payload[:-1]

if __name__ == "__main__":
    def StoreHandle(recv):
        if recv.find("MAIL") >=0:
            print "Sending Mail!!!"
    def FetchHandle(dst, recv):
        if recv.find("TIME") >=0:
            from datetime import datetime
            print "Sending time..."
            sleep(0.25)
            Store(dst, str(datetime.now()))
    Init()
