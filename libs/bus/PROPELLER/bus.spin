CON
  _clkmode = xtal1 + pll16x
  _xinfreq = 5_000_000

  'Pins
  LED = 22
  TX_ENABLE = 14
  RX_ENABLE = 13
  TX = 15
  RX = 12

  'Device address (should be in eeprom)
  SRC = "B"
  RPI = "A"

  'Command constants
  FETCH_CHAR  = "@"
  STORE_CHAR  = "!"
  FETCH_CMD   = 1
  STORE_CMD   = 2
  POLL_CMD    = 3
  CMD_OFFSET  = 4
  DATA_OFFSET = 5

  'Read messages
  SUCCESS         = 0
  LEN_ERROR       = 1
  CHECKSUM_ERROR  = 2
  OWNERSHIP_ERROR = 3


  TIMEOUT = 1000
  BUFFER_SIZE = 128
  BAUDRATE = 9600
   

DAT
{
  Master Pi (A) ---- Slave #1 (B) ----- Slave #2 (C)
  
  <PREAMBLE(NUL)> <DST(A-Z)> <SRC(A-Z)> <LEN> <DATA> <CKSUM>
  1               2          3          4-5   6-     LAST

  
  (M2S POLL)
  NUL B A 00 CKSUM

  (S2M IDLE)
  NUL A B 00 CKSUM

  (S2M STORE) AFTER POLL
  NUL A B LEN !TOPIC/PAR1/PAR2/PAR3... CKSUM 

  (S2M FETCH) AFTER POLL
  NUL A B LEN @TOPIC/PAR1/PAR2/PAR3... CKSUM

  (M2S STORE)
  NUL B A LEN !TOPIC/PAR1/PAR2/PAR3... CKSUM

  (M2S FETCH)
  NUL B A LEN @TOPIC/PAR1/PAR2/PAR3... CKSUM
}
  
OBJ                                        
  pst : "Parallax Serial Terminal"
  ser : "Full_Duplex_Serial"

VAR
  byte WriteBuffer[BUFFER_SIZE]
  byte ReadBuffer[BUFFER_SIZE]
  byte Message[BUFFER_SIZE]

  byte GetTime
  byte SendMail
                                           
PUB Main | i
  Init
  i := 0
  Pause(4000)
  repeat
    i++
    pst.Dec(i)
    pst.Char(":")
    MSGloop  

PUB Init
  dira[LED] := 1
  EnableRX
  DisableTX
  dira[TX_ENABLE] := 1
  dira[RX_ENABLE] := 1
  pst.Start(115200)
  ser.Start(RX, TX, 0, BAUDRATE)
  GetTime := False
  SendMail := False

PUB MSGloop | status, cmd
  status := ReadMSG
  if status == CHECKSUM_ERROR
    pst.Str(string(" Read error "))
    pst.Newline
    return
  if status == LEN_ERROR
    pst.Str(string(" Abnormal length "))    
    pst.Newline
    return
  if status == OWNERSHIP_ERROR
    pst.Str(string(" Not my packet "))
    Idle ' in real life, should not respond
    return

  cmd := Decode
  if cmd == FETCH_CMD
    pst.str(string(" Fetch ")) 
    ParseFetch
  elseif cmd == STORE_CMD
    pst.str(string(" STORE ")) 
    ParseStore
  elseif cmd == POLL_CMD
    pst.str(string(" POLL "))
    if GetTime
      GetTime := False
      SendMSG(string("@TIME"))
    elseif SendMail
      SendMail := False
      SendMSG(string("!MAIL"))      
    else
      Idle 
  
  pst.Str(string(" OK! ")) 
  pst.Newline

PUB ParseStore | dataAddr
  dataAddr := @Message[DATA_OFFSET]
  
  if strcomp(string("LED/ON"), dataAddr)
    LEDon
  if strcomp(string("LED/OFF"), dataAddr)
    LEDoff
  if strcomp(string("TIME"), dataAddr)
    GetTime := True
  if strcomp(string("MAIL"), dataAddr)
    SendMail := True
    
PUB ParseFetch | dataAddr, i
  dataAddr := @Message[DATA_OFFSET]
  i~
  repeat while byte[dataAddr][i] <> $00
    if byte[dataAddr][i] == "/"
      byte[dataAddr][i] := $00
      pst.Dec(i)
    i++      
  pst.Str(dataAddr)
   
  if strcomp(string("HELLO"), dataAddr)
    SendMSG(string("WORLD"))
  if strcomp(string("COUNTER"), dataAddr)
    MakeCnt
  if strcomp(string("MAIL"), dataAddr)
    pst.Str(dataAddr+5)
    pst.Newline
    
PUB MakeCnt | tmp, ptr
  tmp := ||cnt
  ptr := 0
  clear(@Message)
  Message[ptr++] := "!" 
  repeat ptr from 1 to 5
    Message[ptr] := tmp//10 + $30
    tmp/= 10
  Message[ptr] := $00
  SendMSG(@Message)
    
  

PUB Idle
  SendMSG(0)

PUB SendMSG(dataAddr) | char, ptr, len, checkSum, i
  Pause(100)
  Clear(@WriteBuffer)
  ptr := 0
  WriteBuffer[ptr++] := $00 'NUL
  WriteBuffer[ptr++] := RPI 'Always RPi for now
  WriteBuffer[ptr++] := SRC 'Source constant or EEPROM value

  if dataAddr <> 0
    len := strsize(dataAddr)     
    WriteBuffer[ptr++] := (len/10) + $30 'ten  ASCII
    WriteBuffer[ptr++] := (len//10)+ $30 'unit ASCII
      i := 0
    char := $FF
    repeat until char == $00
      char := byte[dataAddr][i++]
      WriteBuffer[ptr++] := char      
    len := ptr-2 're-use len as total len of packet
  else
    WriteBuffer[ptr++] := "0"
    WriteBuffer[ptr++] := "0"
    len := ptr-1    

  checkSum := 0
  repeat i from 1 to len
    char := WriteBuffer[i]
    checkSum := checkSum + char
    pst.char(char)
  
  checkSum &= $FF 'Eliminate overflow
  WriteBuffer[++len] := checkSum 
   
  EnableTX
  repeat i from 0 to len
    ser.tx(WriteBuffer[i]) 
  DisableTX


PUB ReadMSG | char, ptr, len, checkSum, i
  EnableRX
  Clear(@ReadBuffer)
  ptr := 0
  char := $00
  repeat while char == $00 'Wait until beginning
    char := ser.rx
  repeat until char => "A" AND char =< "Z" 'Next char should be an address !!!To check... not supposed to be needed
    char := ser.rx

  ReadBuffer[ptr++] := char   'DST
  ReadBuffer[ptr++] := ser.rx 'SRC
  ReadBuffer[ptr++] := ser.rx 'LEN TEN
  ReadBuffer[ptr++] := ser.rx 'LEN UNIT
  len := 10*(ReadBuffer[2]-$30)+(ReadBuffer[3]-$30) 'Convert LEN from ASCII to binary
  if len<0 OR len>99
    return LEN_ERROR
  
  repeat until ptr == (len+5) 'until end of packet received
    ReadBuffer[ptr++] := ser.rx

  len := ptr-1 're-use len as total len of packet
  ptr := 0     're-use ptr as loop counter
  checkSum := 0
  repeat len
    char := ReadBuffer[ptr++]
    checkSum := checkSum + char
    'pst.char(char)
  
  checkSum &= $FF 'Eliminate overflow
  if checkSum <> ReadBuffer[ptr]
    return CHECKSUM_ERROR

  if ReadBuffer[0] <> SRC
    return OWNERSHIP_ERROR
        
  Clear(@Message)
  bytemove(@Message, @ReadBuffer, len)
  return SUCCESS
  DisableRX

PUB Decode : cmd
  pst.Str(@Message)
  if Message[CMD_OFFSET] == FETCH_CHAR
    cmd := FETCH_CMD
  elseif Message[CMD_OFFSET] == STORE_CHAR
    cmd := STORE_CMD
  else
    cmd := POLL_CMD
  return cmd

PUB Clear(bufferAddr)
  bytefill(bufferAddr, 0, BUFFER_SIZE)

PUB LEDon
  outa[LED] := 1

PUB LEDoff
  outa[LED] := 0

PUB EnableTX
  outa[TX_ENABLE] := 1

PUB DisableTX
  Pause(200) 'Do not disable too soon, we need to finish tx before
  outa[TX_ENABLE] := 0

PUB EnableRX
  outa[RX_ENABLE] := 0
  Pause(200) 'Wait until its really enabled

PUB DisableRX
  outa[RX_ENABLE] := 1
  Pause(200) 'Wait until its really disabled

PUB Pause(ms)
  waitcnt(clkfreq/1000 * ms + cnt)
  