#include <Servo.h>

String myCmd;

Servo myServo;

void setup() {
  // Starts the Serial
  Serial.begin(9600);
  Serial.setTimeout(10);

  // Attaches the servo
  myServo.attach(9);

  // Inits the servo
  myServo.write(90); 
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available() == 0) {
    pinMode(13, OUTPUT);
  }
  myCmd = Serial.readStringUntil('\r');
  if (myCmd[1] == 'n') {
    digitalWrite(13, HIGH);
    myServo.write(180);
  }
  else if (myCmd[2] == 'f') {
    digitalWrite(13, LOW);
    myServo.write(0);
  }
  else if (myCmd[0] == '1') {
    myServo.write(90);
  }
}