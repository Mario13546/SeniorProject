// Imports
#include <Servo.h>

// Objects
Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;

// Variables
String myString;

// Setup code goes here
void setup() {
  // Starts the serial
  Serial.begin(9600);
  Serial.setTimeout(10);

  // Sets up the servos
  servoThumb .attach(8);
  servoIndex .attach(9);
  servoMiddle.attach(10);
  servoRing  .attach(11);
  servoPinky .attach(12);

  // Servos go to the init position (middle)
  servoThumb .write(180);
  servoIndex .write(180);
  servoMiddle.write(180);
  servoRing  .write(180);
  servoPinky .write(180);
}

// Main loop code goes here
void loop() {
  // Idles when there is no data
  while (Serial.available() == 0) { }

  // Recieves the data
  myString = Serial.readStringUntil('\r');

  // Thumb movement
  if (myString[0] == '1') {
    servoThumb.write(180);
  }
  else {
    servoThumb.write(0);
  }

  // Index movement
  if (myString[1] == '1') {
    servoIndex.write(180);
  }
  else {
    servoIndex.write(0);
  }

  // Middle movement
  if (myString[2] == '1') {
    servoMiddle.write(180);
  }
  else {
    servoMiddle.write(0);
  }

  // Ring movement
  if (myString[3] == '1') {
    servoRing.write(180);
  }
  else {
    servoRing.write(0);
  }

  // Pinky movement
  if (myString[4] == '1') {
    servoPinky.write(180);
  }
  else {
    servoPinky.write(0);
  }
}