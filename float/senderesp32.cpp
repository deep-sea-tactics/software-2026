//This file is for the esp32 that will be used to send data from the sensor and control the servo accordingly. 
// It will be in access point mode to send data to the receiver esp32.
//It will be in the float
//DO NOT USE THIS FILE AND EXECUTE IT, THIS IS ONLY FOR SHOWING THE CODE
#include <ESP32Servo.h>
#include "MS5837.h"
#include <Wire.h>
#include <esp_now.h>
#include <WiFi.h>



Servo myServo;
int servoPin = 14;
MS5837 sensor;


int depth = 2;
int target_depth[] = {2,30,50}; //in meters
int current_target;
unsigned long startTime = millis();


void setup() {
  Serial.begin(115200);
  // Allow allocation of all timers
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  ESP32PWM::allocateTimer(2);
  ESP32PWM::allocateTimer(3);
  Serial.println("Initializing PWM pins");
 
  myServo.setPeriodHertz(50); // Standard 50hz servo
  myServo.attach(servoPin,500, 2500); // Attach with standard PWM pulse widths
  Serial.println("Starting servo 360 test...");

  Serial.println("Initializing Bar02 sensor");
  Wire.begin();
  sensor.setModel(MS5837::MS5837_02BA);  //Change to MS5837::MS5837_30BA if using Bar30
  sensor.init();
  sensor.setFluidDensity(997); // kg/m^3 (997 freshwater, 1029 seawater)


}


void loop() {
  // 360 Servo Control:
  // 90 is typically stop
  // 0 is full speed one way
  // 180 is full speed the other way  
  /*
  for (int i: target_depth){
    current_target == target_depth[i]
    if (current_target == target_depth[i]) {
    while (depth < current_target){
      //servo.spin //whichever way it spins to absorb water //NOT REAL CODE
    }
    else if (depth == current_target){
	  myServo.write(1500);
	  delay(1000);
      while(millis() - startTime < 30000){
      //get pressure, temp, depth, etc for 30 sec


    }
    delay(10);
    while(depth > 0){
    myServo.write(int)//spin other way
    }
  
    else if (depth <= 0){
	  myServo.write(90);
	  delay(100);
	  //send data type shi via wireless
	  //idfk how to send shi (esp32)


  }
  }


  }
  */
 


  Serial.println("Moving Clockwise");
  myServo.writeMicroseconds(1100); // stop value - 400 
  delay(2000); // Increased delay to observe movement


  Serial.println("Stopping");
  myServo.writeMicroseconds(1500); // If it still creeps, and if cw, +100/10/1 increments till full stop; if ccw, -100/10/1 increments till full stop ie 1085
  delay(2000);
  //while(true);
  Serial.println("Moving Counter-Clockwise");
  myServo.writeMicroseconds(1900); // stop value + 400 
  delay(2000);


  //Serial.println("Stopping");




}