#include <Servo.h>

#define numOfValsRec 5

// Objects
Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;

// Variables
int valsRec[numOfValsRec];
String recievedString;

// Setup code goes here
void setup() {
  // Starts the serial
  Serial.begin(9600);
  Serial.setTimeout(10);

  // Sets up the servos
  servoThumb .attach(7);
  servoIndex .attach(8);
  servoMiddle.attach(9);
  servoRing  .attach(10);
  servoPinky .attach(11);

  // Servos go to the init position (middle)
  servoThumb .write(90);
  servoIndex .write(90);
  servoMiddle.write(90);
  servoRing  .write(90);
  servoPinky .write(90);
}

// Main loop code goes here
void loop() {
  // Recieves the data
  recieveData();

  // Thumb movement
  if (valsRec[0] == 1) {
    servoThumb.write(180);
  }
  else {
    servoThumb.write(0);
  }

  // Index movement
  if (valsRec[1] == 1) {
    servoIndex.write(180);
  }
  else {
    servoIndex.write(0);
  }

  // Middle movement
  if (valsRec[2] == 1) {
    servoMiddle.write(180);
  }
  else {
    servoMiddle.write(0);
  }

  // Ring movement
  if (valsRec[3] == 1) {
    servoRing.write(180);
  }
  else {
    servoRing.write(0);
  }

  // Pinky movement
  if (valsRec[4] == 1) {
    servoPinky.write(180);
  }
  else {
    servoPinky.write(0);
  }
}

void recieveData() {
  // Stores the serial value in recievedString
  recievedString = Serial.readString();

  // Sets the value of recievedString
  for (int i; i < numOfValsRec; i++) {
    String temp = recievedString.subString(i, i + 1);
    valsRec[i] = temp.toInt();
  }

  // Resets values
  recievedString = "";
}
