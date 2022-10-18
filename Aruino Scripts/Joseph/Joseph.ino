#include <Servo.h>
Servo servo;

void setup(){
  servo.attach(A0);
  Serial.begin(9600);
  Serial.setTimeout(10);
  servo.write(39);
}

void loop(){  
  //while(Serial.available()==0){}
  String data = Serial.readString();
  int value = data.toInt();
  
  if(value!=91) {
    servo.write(value);
    
    servo.write(data.toInt());
    delay(15);
  }
  if(value==91) {
    servo.write(39);
  }
}
