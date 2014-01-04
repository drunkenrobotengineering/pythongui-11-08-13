// Modified by Worapoht K.
#include <SoftwareSerial.h>

int  val = 0; 
char code[10];
char old_code[10] = {' ',' ',' ',' ',' ',' ',' ',' ',' ',' '};
int bytesread = 0; 

#define rxPin 8
#define txPin 9
// RFID reader SOUT pin connected to Serial RX pin at 2400bps to pin8

SoftwareSerial RFID = SoftwareSerial(rxPin,txPin);

void setup()
{
  delay(5000);
  Serial.begin(2400);  // Hardware serial for Monitor 2400bps

  pinMode(2,OUTPUT);       // Set digital pin 2 as OUTPUT to connect it to the RFID /ENABLE pin 
  digitalWrite(2, LOW);    // Activate the RFID reader 
  RFID.begin(2400);
}


void loop()
{ 

  if((val = RFID.read()) == 10)
  {   // check for header 
    bytesread = 0; 
    while(bytesread<10)
    {  // read 10 digit code 
      val = RFID.read(); 
      if((val == 10)||(val == 13))
      {  // if header or stop bytes before the 10 digit reading 
        break;                       // stop reading 
      } 
      code[bytesread] = val;         // add the digit           
      bytesread++;                   // ready to read next digit  
    } 

    if(bytesread == 10 && !isCodeSame())
    {  // if 10 digit read is complete 
      if (isCodeValid()) {
        Serial.print("TAG code is: ");   // possibly a good TAG 
        Serial.println(code);            // print the TAG code 
        setOld();
      }
    }
    bytesread = 0; 
    delay(250);                       // wait for a second
  } 
}

boolean isCodeSame() {
  boolean isSame = true;
  for (int i = 0; i < 10; i++) {
    if (code[i] != old_code[i]) {
      isSame = false;
    }
  }
  return isSame;
}

boolean isCodeValid() {
  boolean isValid = true;
  for (int i = 0; i < 10; i++) {
    if (!isHex(code[i])) {
      isValid = false;
    }
  }
  return isValid;  
}

boolean isHex(char c) {
  int i = (int) c;
  return (i > 47 && i < 58) || (i > 64 && i < 71) || (i > 96 && i < 103);
}

void setOld() {
  for (int i = 0; i < 10; i++) {
    old_code[i] = code[i];
  }
}

