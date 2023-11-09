// Declare variables
int photoResValue = 0;





void setup() {
  // put your setup code here, to run once:
  pinMode(A0, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  // Read value from photo resistor
  photoResValue = analogRead(A0);

  // Print value of photoresistor
  Serial.println(photoResValue);
}
