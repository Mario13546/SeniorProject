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
  servoRotate.write( 90);
  servoThumb .write(180);
  servoIndex .write(180);
  servoMiddle.write(180);
  servoRing  .write(180);
  servoPinky .write(180);

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

  // Sets the number of digits per number
  numDigits = int(myString[0]);

  // Sets up the indices
  index   = 1;
  indexUp = index + numDigits;

  // Thumb movement
  if (myString.substring(index, indexUp).toInt() != 0) {
    servoThumb.write(int(myString[0]));
  }
  else {
    servoThumb.write(0);
  }

  // Increments the indices
  index   += 3;
  indexUp += 3;

  // Index movement
  if (myString.substring(index, indexUp).toInt() != 0) {
    servoIndex.write(int(myString[1]));
  }
  else {
    servoIndex.write(0);
  }

  // Increments the indices
  index   += 3;
  indexUp += 3;

  // Middle movement
  if (myString.substring(index, indexUp).toInt() != 0) {
    servoMiddle.write(int(myString[2]));
  }
  else {
    servoMiddle.write(0);
  }

  // Increments the indices
  index   += 3;
  indexUp += 3;

  // Ring movement
  if (myString.substring(index, indexUp).toInt() != 0) {
    servoRing.write(int(myString[3]));
  }
  else {
    servoRing.write(0);
  }

  // Increments the indices
  index   += 3;
  indexUp += 3;

  // Pinky movement
  if (myString.substring(index, indexUp).toInt() != 0) {
    servoPinky.write(int(myString[4]));
  }
  else {
    servoPinky.write(0);
  }
}