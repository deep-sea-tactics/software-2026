//This file is for the other esp32 that will be used and it will be in station mode to receive data from the sender esp32.
//DO NOT USE THIS FILE AND EXECUTE IT, THIS IS ONLY FOR SHOWING THE CODE

#include <esp_now.h>
#include <WiFi.h>

// --- Mirror Exact Sender Packet Struct Form Factor ---
struct DataPacket {
  uint16_t packetId;
  float depth;
  float pressureKpa;
  uint32_t timeElapsed;
  char status[16];
};

// Callback triggered whenever an ESP-NOW data chunk settles into the receiver stack
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  DataPacket packet;
  memcpy(&packet, incomingData, sizeof(packet));
  
  if (packet.packetId == 0) {
    Serial.println("\n--- ALERT: PRE-DESCENT NOTICE DETECTED ---");
    Serial.printf("Initial Depth Check: %.2f m | Station Pressure: %.2f kPa\n", packet.depth, packet.pressureKpa);
    Serial.println("-------------------------------------------\n");
    // Print table header row immediately following confirmation
    Serial.println("PKT_ID , DEPTH(m) , PRESSURE(kPa) , TIME_ELAPSED(ms) , CURRENT_STATE");
  } else {
    // Outputs clean CSV structural formatting for instant copying into Excel charts
    Serial.printf("%d , %.2f , %.2f , %u , %s\n", 
                  packet.packetId, 
                  packet.depth, 
                  packet.pressureKpa, 
                  packet.timeElapsed, 
                  packet.status);
  }
}

void setup() {
  Serial.begin(115200);
  
  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);

  // Initialize ESP-NOW Protocol
  if (esp_now_init() != ESP_OK) {
    Serial.println("Critical Failure: ESP-NOW failed initialization on Base Station.");
    return;
  }
  
  // Bind callback pipeline logic
  esp_now_register_recv_cb(esp_now_recv_cb_t(OnDataRecv));
  Serial.println("Base Surface System Online. Awaiting Profile Broadcasts...");
}

void loop() {
  // Keeps microcontroller execution open for handling inbound network frames
  delay(100);
}
