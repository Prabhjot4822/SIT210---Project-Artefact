#include <Servo.h>

String command;

Servo thumb;
Servo index;
Servo middle;
Servo ring;
Servo small;

int pos = 0;

void setup() {
  Serial.begin(9600);
  thumb.attach(6);
  index.attach(7);
  middle.attach(3);
  ring.attach(8);
  small.attach(5);
}

void loop() 
{
  if (Serial.available()) 
  {
    command = Serial.readStringUntil('\n');
    command.trim();
    if (command.equals("one")) 
    {
      digitalWrite(whiteLed, HIGH);
      digitalWrite(blueLed, LOW);
      digitalWrite(redLed, LOW);
    }

    else if (command.equals("blue")) {
      digitalWrite(whiteLed, LOW);
      digitalWrite(blueLed, HIGH);
      digitalWrite(redLed, LOW);
    }
  }

  delay(1000);
}
