BYTE testme(BYTE input)
{
        BYTE retval = 0;

        if (input == 0x55)
        {
                retval =  0xAA;
        }

        return retval;
}

void delayus(DWORD us) 
{
	// Here will go the code to make a 'us' microseconds delay
	
}


void delayms(DWORD ms) 
{
	// Here will go the code to make a 'ms' miliseconds delay
	
}

void randomDelay(DWORD us) 
{
	// Here will go the code to make a random delay up to 'us' microseconds.
	
}