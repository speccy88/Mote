#include "../utils/utils.h"

BYTE testme(BYTE input)
{
        BYTE retval = 0;

        if (input == 0x55)
        {
                retval =  0xAA;
        }

        return retval;
}


BOOL SendByte(DEVICE_ID to, BYTE input){
	BOOL retval = FAIL;
	return retval;
}

BYTE ReceiveByte(DEVICE_ID from){

}

BOOL SendWord(DEVICE_ID to, WORDinput){
	BOOL retval = FAIL;
	return retval;
}
WORD ReceiveWord(DEVICE_ID from);


BOOL SendCommand(DEVICE_ID to, COMMAND command){
	BOOL retval = FAIL;
	return retval;
}
COMMAND ReceiveCommand(DEVICE_ID from);

