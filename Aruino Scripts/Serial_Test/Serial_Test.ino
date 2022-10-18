// Imports
#include <Servo.h>

// Object Creation
Servo servo;

// Variables
int const servoPin = 9
int value = 0

void setup() {
  // Starts serial communications
  Serial.begin(9600);
  Serial.setTimeout(10);

  // Attaches the servo to port 9
  servo.attach(servoPin);

  // Sets the servo to init to the middle
  servo.write(90);
}

void loop() {  
  String data = Serial.readString();
  value = data.toInt();
  
  // Value outside of tolerable range
  if (value > 179 || value < 0) {
    // Goes to middle point
    servo.write(90);
  }
  // Value inside tolerable range
  else {
    // Goes to the value
    servo.write(value);
  }
}