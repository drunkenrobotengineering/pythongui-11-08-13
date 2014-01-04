int flow_sensors[2] = {2,4};

volatile uint16_t pulses[2] = {0,0};
volatile uint8_t lastflowpinstate[2];

void readFlow(int i) {
    uint8_t x = digitalRead(flow_sensors[i]);  
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
  Serial.print("Flow sensor test!");
  for (int i = 0; i < 2; i++){
    pinMode(flow_sensors[i], INPUT);
    digitalWrite(flow_sensors[i], HIGH);
    lastflowpinstate[i] = digitalRead(flow_sensors[i]);
  }
  useInterrupt(true);
}

void loop()
{ 
  float liters1 = pulses[0] / (7.5*60.0);
  float liters2 = pulses[1] / (7.5*60.0);
  while (Serial.available() > 0) {
    while (Serial.available() > 0) {Serial.read();}  
    Serial.print("{\"1\":{\"c\":"); + Serial.print(liters1 * 1000); Serial.print("},\"2\":{\"c\":"); Serial.print(liters2 * 1000); Serial.println("}}");
  }
}