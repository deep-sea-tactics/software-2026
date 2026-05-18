//This file is for the esp32 that will be used to send data from the sensor and control the servo accordingly. 
// It will be in access point mode to send data to the receiver esp32.
//It will be in the float
//DO NOT USE THIS FILE AND EXECUTE IT, THIS IS ONLY FOR SHOWING THE CODE
#include <esp_now.h>
#include <WiFi.h>
#include <Wire.h>
#include "MS5837.h"
#include <ESP32Servo.h>

// --- Configuration Pins & Constants ---
#define SERVO_PIN 14
#define SERVO_STOP 1500 // Neutral value for your 360 continuous servo

// --- Target Profiles ---
const float TARGET_DEPTH_1 = 0.40; 
const float TARGET_DEPTH_2 = 2.50; 
const unsigned long HOVER_DURATION = 30000; 

// --- PID Tuning Parameters ---
// Adjust these during testing. 
// Kp: Aggression on error. Ki: Fixes steady-state offset. Kd: Damps oscillations.
float Kp = 40.0;  
float Ki = 5.0;   
float Kd = 15.0;  

float pidIntegratedError = 0;
float pidLastError = 0;
unsigned long lastPidTime = 0;

// --- ESP-NOW Configuration ---
uint8_t broadcastAddress[] = {0x1C, 0xC3, 0xAB, 0xBA, 0x83, 0x4C};

struct DataPacket {
  uint16_t packetId;
  float depth;          
  float pressureKpa;    
  uint32_t timeElapsed; 
  char status[15];      
};

DataPacket diveLog[100]; 
int packetCounter = 0;

MS5837 depthSensor;
Servo ballastServo;

enum FloatState { PRE_DESCENT, DESCENT_PROFILE_1, DESCENT_PROFILE_2, WAITING_FOR_RECOVERY, RECOVERY_TRANSMISSION };
FloatState currentState = PRE_DESCENT;

unsigned long descentStartTime = 0;
unsigned long lastLogTime = 0;
unsigned long surfaceTimer = 0;
int profileIteration = 1; 

// Smooth PID computation for continuous rotation servo
void updatePID(float currentDepth, float targetDepth) {
  unsigned long now = millis();
  float dt = (now - lastPidTime) / 1000.0; // Time step in seconds
  if (dt <= 0) return;
  lastPidTime = now;

  float error = targetDepth - currentDepth; // Positive means need to sink
  
  // Proportional term
  float pTerm = Kp * error;

  // Integral term (with anti-windup clamping)
  pidIntegratedError += error * dt;
  pidIntegratedError = constrain(pidIntegratedError, -20, 20); 
  float iTerm = Ki * pidIntegratedError;

  // Derivative term
  float dTerm = Kd * ((error - pidLastError) / dt);
  pidLastError = error;

  // Combine terms to create a servo speed offset
  float pidOutput = pTerm + iTerm + dTerm;

  // Map PID output to servo write range (1100 to 1900 speed range)
  // Positive output = sink (servo forward), Negative output = rise (servo reverse)
  int servoCommand = SERVO_STOP + constrain((int)pidOutput, -400, 400);
  
  ballastServo.writeMicroseconds(servoCommand);
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW Init Failed");
    return;
  }

  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  esp_now_add_peer(&peerInfo);

  Wire.begin();
  if (!depthSensor.init()) {
    Serial.println("Bar02 Init Failed! ");
    while (1);
  }
  depthSensor.setModel(MS5837::MS5837_02BA);
  depthSensor.setFluidDensity(997); 

  ESP32PWM::allocateTimer(0);
  ballastServo.setPeriodHertz(50);
  ballastServo.attach(SERVO_PIN, 1000, 2000);
  ballastServo.writeMicroseconds(SERVO_STOP);
  lastPidTime = millis();
}

void loop() {
  depthSensor.read();
  float currentDepth = depthSensor.depth();
  float currentPressureKpa = depthSensor.pressure() * 0.1; 

  switch (currentState) {
    
    case PRE_DESCENT: {
      DataPacket preDescentPacket = {0, currentDepth, currentPressureKpa, 0, "PRE_DESCENT"};
      esp_now_send(broadcastAddress, (uint8_t *) &preDescentPacket, sizeof(preDescentPacket));
      
      delay(2000); 
      descentStartTime = millis();
      lastLogTime = millis();
      lastPidTime = millis();
      currentState = DESCENT_PROFILE_1;
      break;
    }

    case DESCENT_PROFILE_1: {
      updatePID(currentDepth, TARGET_DEPTH_1);
      
      if (millis() - lastLogTime >= 5000) {
        lastLogTime = millis();
        diveLog[packetCounter] = { (uint16_t)(packetCounter + 1), currentDepth, currentPressureKpa, (uint32_t)(millis() - descentStartTime), "PROFILE_1" };
        packetCounter++;
      }

      if (millis() - descentStartTime >= (HOVER_DURATION * profileIteration)) {
        pidIntegratedError = 0; // Reset integral for new depth target
        currentState = DESCENT_PROFILE_2;
      }
      break;
    }

    case DESCENT_PROFILE_2: {
      updatePID(currentDepth, TARGET_DEPTH_2);

      if (millis() - lastLogTime >= 5000) {
        lastLogTime = millis();
        diveLog[packetCounter] = { (uint16_t)(packetCounter + 1), currentDepth, currentPressureKpa, (uint32_t)(millis() - descentStartTime), "PROFILE_2" };
        packetCounter++;
      }

      if (millis() - descentStartTime >= ((HOVER_DURATION * 2) * profileIteration)) {
        pidIntegratedError = 0;
        if (profileIteration < 2) {
          profileIteration++; 
          currentState = DESCENT_PROFILE_1; 
        } else {
          currentState = WAITING_FOR_RECOVERY;
        }
      }
      break;
    }

    case WAITING_FOR_RECOVERY: {
      // Command servo to rise back to the surface completely
      updatePID(currentDepth, 0.0); 
      
      // Make sure we have at least 22 packets recorded to meet rules safely
      while(packetCounter < 22) {
         diveLog[packetCounter] = { (uint16_t)(packetCounter + 1), currentDepth, currentPressureKpa, (uint32_t)(millis() - descentStartTime), "POST_DIVE" };
         packetCounter++;
      }

      // Automated Recovery Trigger: If depth is near 0 for 5 consecutive seconds
      if (currentDepth < 0.05) {
        if (surfaceTimer == 0) {
          surfaceTimer = millis();
        } else if (millis() - surfaceTimer >= 5000) {
          ballastServo.writeMicroseconds(SERVO_STOP); // Turn off motor
          currentState = RECOVERY_TRANSMISSION;
        }
      } else {
        surfaceTimer = 0; // Reset timer if it dips below surface again
      }
      break;
    }

    case RECOVERY_TRANSMISSION: {
      ballastServo.writeMicroseconds(SERVO_STOP);
      
      for (int i = 0; i < packetCounter; i++) {
        esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &diveLog[i], sizeof(diveLog[i]));
        delay(40); 
      }
      
      while(1); // Lock program execution to prevent repeating burst transmission
      break;
    }
  }
  delay(10);
}
