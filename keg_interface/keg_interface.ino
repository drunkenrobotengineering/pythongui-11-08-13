#include <SoftwareSerial.h>
int FLOW[2] = {2,3};
int KEGS[2] = {4,5};
int RFID_CTRL = 7;
int RFID_RX = 8;
int RFID_TX = 9;
int OVERRIDE = 10;

int DEBUG_SWITCH = 11;

int LOOP_WAIT = 500;
int TIMEOUT_SECONDS = 5;
int TIMEOUT_LOOPS = TIMEOUT_SECONDS * 1000 / LOOP_WAIT;

boolean engaged = false;

int loops_since_last_pull = 0;
uint16_t previous_pulses[2] = {0,0};
uint16_t pulses_before_dispensing[2] = {0,0};

int  val = 0;
char code[10];
char old_code[10] = {' ',' ',' ',' ',' ',' ',' ',' ',' ',' '};
int bytesread = 0; 

SoftwareSerial RFID = SoftwareSerial(RFID_RX, RFID_TX);

volatile uint16_t pulses[2] = {0,0};
volatile uint8_t lastflowpinstate[2];

void readFlow(int i) {
    uint8_t x = digitalRead(FLOW[i]);  
    if (x == lastflowpinstate[i]) {return;}
    if (x == HIGH) {pulses[i]++;}
    lastflowpinstate[i] = x;
}

SIGNAL(TIMER0_COMPA_vect) {
  readFlow(0);
  readFlow(1);
}

void useInterrupt(boolean v) {
  if (v) {
    // Timer0 is already used for millis() - we'll just interrupt somewhere
    // in the middle and call the "Compare A" function above
    OCR0A = 0xAF;
    TIMSK0 |= _BV(OCIE0A);
  } else {
    // do not call the interrupt function COMPA anymore
    TIMSK0 &= ~_BV(OCIE0A);
  }
}

void setup() {
  Serial.begin(19200);
  debug("Setting up everything...");
  for (int i = 0; i < 2; i++){
    pinMode(FLOW[i], INPUT);
    digitalWrite(FLOW[i], HIGH);
    lastflowpinstate[i] = digitalRead(FLOW[i]);
    pinMode(KEGS[i], OUTPUT);
    digitalWrite(KEGS[i], LOW);
  }
  lock();
  useInterrupt(true);
  pinMode(OVERRIDE, INPUT);
  pinMode(DEBUG_SWITCH, INPUT);
  pinMode(RFID_CTRL, OUTPUT);
  digitalWrite(RFID_CTRL, LOW);
  RFID.begin(2400);
  debug("Done with setup.");
}

void loop()
{
  if (overridden()) {
    debug("Override enabled.");
    unlock();
  } else {
    if (!engaged) {
       debug("NOT ENGAGED.");
       notDispensing();
    } else {
      debug("ENGAGED.");
      dispensing();
    }
  }
  delay(LOOP_WAIT);
}

void notDispensing() {
  // Wait for an RFID card to be inserted.
  if((val = RFID.read()) == 10)
    {   
    debug(String(val));
    // check for header 
    bytesread = 0; 
    while(bytesread<10)
    {  // read 10 digit code 
      val = RFID.read(); 
      debug(String(val));
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
        debug("Just read a new code:");
        debug(code);
        setOld();
        begin_dispensing();
      }
    }
    bytesread = 0; 
  } else {
    debug(String(val));
  }

}

void dispensing() {
    if (previous_pulses[0] != pulses[0] || previous_pulses[1] != pulses[1]) {
      previous_pulses[0] = pulses[0];
      previous_pulses[1] = pulses[1];
      loops_since_last_pull = 0;
    } else {
      debug("Dispensing.  Loops since last pull:");
      debug(String(loops_since_last_pull));
      loops_since_last_pull++;
    }
    if (loops_since_last_pull >= TIMEOUT_LOOPS) {
      // It's been about 10 seconds since the last bit of beer was dispensed.
      end_dispensing();
    }
}

void begin_dispensing() {
  debug("begin_dispensing called.");
  if (!verify_access_permissions()) {
    // The code doesn't check out - don't turn on the tap.
    return;
  }
  pulses_before_dispensing[0] = pulses[0];
  pulses_before_dispensing[1] = pulses[1];
  previous_pulses[0] = pulses_before_dispensing[0];
  previous_pulses[1] = pulses_before_dispensing[1];
  loops_since_last_pull = 0;
  digitalWrite(RFID_CTRL, HIGH);
  engaged = true;
  unlock();
}

void end_dispensing() {
  debug("end_dispensing called.");
  lock();
  float liters1 = (pulses[0] - pulses_before_dispensing[0]) / (7.5*60.0);
  float liters2 = (pulses[1] - pulses_before_dispensing[1]) / (7.5*60.0);
  send_data(liters1, liters2);
  pulses_before_dispensing[0] = pulses[0];
  pulses_before_dispensing[1] = pulses[1];
  previous_pulses[0] = pulses_before_dispensing[0];
  previous_pulses[1] = pulses_before_dispensing[1];
  loops_since_last_pull = 0;
  zeroize_codes();
  while (RFID.read() >= 0) {
      // Empty the buffer
  }
  digitalWrite(RFID_CTRL, LOW);
  engaged = false;
}

void zeroize_codes() {
  for (int i = 0; i < 10; i++) {
    code[i] = ' ';
    old_code[i] = ' ';
  }
}

boolean verify_access_permissions() {
  debug("Verifying permissions for code ");
  debug(code);
  // This method could be used to check access control
  // Currently anyone with an RFID chip of the right type can get access
  // This call could, for example, implement a whitelist or a blacklist.
  // It could even call out to the RPi with the code to check something like age of the owner or how much they've had to drink recently.
  // For now, though, we'll assume everyone is allowed to drink.
  return true;
}

void send_data(float liters1, float liters2) {
  Serial.print("{\"CODE\":\"");
  Serial.print(code);
  Serial.print("\", \"TAP_ONE\":");
  Serial.print(liters1 * 1000);
  Serial.print(",\"TAP_TWO\":");
  Serial.print(liters2 * 1000);
  Serial.println("}");
  }

boolean overridden() {
  if (digitalRead(OVERRIDE) == HIGH) {
    return true;
  }
  return false;
}

void unlock()
{
  debug("unlock called.");
  for (int i = 0; i < 2; i++) {
    digitalWrite(KEGS[i], HIGH);
  }
}

void lock()
{
  debug("lock called.");
  for (int i = 0; i < 2; i++) {
    digitalWrite(KEGS[i], LOW);
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

void debug(String message) {
  if (digitalRead(DEBUG_SWITCH) == HIGH)
  Serial.println(message);
}
