// base pin is connected to digital 2
// collector goes to 5v
// emitter goes to gnd

void setup()
{
  pinMode(2,OUTPUT); 
  digitalWrite(2, LOW); 
  pinMode(1,OUTPUT); 
  digitalWrite(1, LOW); 
}


void loop()
{ 
  delay(1500); 
  digitalWrite(2, HIGH); 
  digitalWrite(1, HIGH); 
  delay(1500);
  digitalWrite(2, LOW);
  digitalWrite(1, LOW);
}
