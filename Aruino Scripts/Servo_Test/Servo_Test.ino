#include<Servo.h>
Servo myServo;

// Variables
int const potPin = A0;
int potVal;
int angle;

// Set Up code
void setup() {
  // Attaches the servo
  myServo.attach(9);

  // Starts the serial
  Serial.begin(9600);
  Serial.setTimeout(10);

  // Init positions
  myServo.write(90);
}

// Main loop
void loop() {
  potVal = analogRead(potPin);
  //Serial.println(potVal);
  
  angle = map(potVal, 0, 1023, 0, 179);
  Serial.println(angle);
  
  myServo.write(angle);
  delay(100);
}
