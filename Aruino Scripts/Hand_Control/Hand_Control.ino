// Imports
#include <Servo.h>

// Objects
Servo servoRotate;
Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;

// Variables
int index;
int indexUp;
int numDigits;
int fingerPos;
String myString;

// Setup code goes here
void setup() {
  // Starts the serial
  Serial.begin(9600);
  Serial.setTimeout(10);

  // Sets up the servos
  servoRotate.attach(7);
  servoThumb .attach(8);
  servoIndex .attach(9);
  servoMiddle.attach(10);
  servoRing  .attach(11);
  servoPinky .attach(12);

  // Servos go to the init position
  servoRotate.write(90);
  servoThumb .write(90);
  servoIndex .write(90);
  servoMiddle.write(90);
  servoRing  .write(90);
  servoPinky .write(90);

  // Initialize the built in LED
  pinMode(LED_BUILTIN, OUTPUT);
}

// Main loop code goes here
void loop() {
  // Idles when there is no data
  while (Serial.available() == 0) {
    // Turns the built in LED off when there is no serial data
    digitalWrite(LED_BUILTIN, LOW);
  }

  // Turns the built in LED on when there is serial data
  digitalWrite(LED_BUILTIN, HIGH);

  // Recieves the data
  myString = Serial.readStringUntil('\r');

  // Sets the digits per number
  numDigits = 3;

  // Sets up the indices
  index   = 0;
  indexUp = index + numDigits;

  // Thumb movement
  if (myString.substring(index, indexUp).toInt() != 0) {
    servoThumb.write(myString.substring(index, indexUp).toInt());
  }
  else {
    servoThumb.write(0);
  }

  // Increments the indices
  index   += numDigits;
  indexUp += numDigits;

  // Index movement
  if (myString.substring(index, indexUp).toInt() != 0) {
    servoIndex.write(myString.substring(index, indexUp).toInt());
  }
  else {
    servoIndex.write(0);
  }

  // Increments the indices
  index   += numDigits;
  indexUp += numDigits;

  // Middle movement
  if (myString.substring(index, indexUp).toInt() != 0) {
    servoMiddle.write(myString.substring(index, indexUp).toInt());
  }
  else {
    servoMiddle.write(0);
  }

  // Increments the indices
  index   += numDigits;
  indexUp += numDigits;

  // Ring movement
  if (myString.substring(index, indexUp).toInt() != 0) {
    servoRing.write(myString.substring(index, indexUp).toInt());
  }
  else {
    servoRing.write(0);
  }

  // Increments the indices
  index   += numDigits;
  indexUp += numDigits;

  // Pinky movement
  if (myString.substring(index, indexUp).toInt() != 0) {
    servoPinky.write(myString.substring(index, indexUp).toInt());
  }
  else {
    servoPinky.write(0);
  }
}