#include <Servo.h>

#define numOfValsRec 5
#define digitsPerValRec 1

// Objects
Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;

// Variables
int valsRec[numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1; //$00000
int counter = 0;
bool counterStart = false;
String recievedString;

// Setup code goes here
void setup() {
  // Starts the serial
  Serial.begin(9600);
  Serial.timout(10);

  // Sets up the servos
  servoThumb.attach(7);
  servoIndex.attach(9);
  servoMiddle.attach(11);
  servoRing.attach(8);
  servoPinky.attach(10);
}

// Main loop code goes here
void loop() {
  // Placeholder
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
  while (Serial.available() == true) {
    char c = Serial.read();

    if (c == '$') {
      counterStart = true;
    }

    if (counterStart == true) {
      if (counter < stringLength) {
        recievedString = String(recievedString + c);
        counter++;
      }
      else {
        for (int i; i < numOfValsRec; i++) {
          int num = (i * digitsPerValRec) + 1;
          valsRec[i] = recievedString.substring(num, num + digitsPerValRec).toInt();
        }

        // Resets values
        recievedString = "";
        counterStart = false;
        counter = 0;
      }
    }
  } 
}
