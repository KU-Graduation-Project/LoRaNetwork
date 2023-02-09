#include <ArduinoBLE.h>
#include <LSM6DS3.h>
#include <Wire.h>

#define CONVERT_TO_MS2    9.80665f
#define MAX_ACCEPTED_RANGE  2.0f

LSM6DS3 myIMU(I2C_MODE, 0x6A);
static bool debug_nn = false;

BLEService myService("fff0");
BLEShortCharacteristic accelerometerCharacteristic_X("2101", BLERead | BLEBroadcast);


void setup() {
  BLE.begin();
  myIMU.begin();

   BLE.setLocalName("Test sensor");
   
  myService.addCharacteristic(accelerometerCharacteristic_X);
  accelerometerCharacteristic_X.writeValue(0);
   
  BLE.addService(myService);

  BLE.advertise();

}

void loop() {
  BLEDevice central = BLE.central();

  if(central.connected()){
    digitalWrite(LED_BUILTIN, HIGH);
  }

  const uint32_t BLE_UPDATE_INTERVAL = 10;
  static uint32_t previousMillis = 0;
  uint32_t currentMillis = millis();
  
  if (currentMillis - previousMillis >= BLE_UPDATE_INTERVAL) {
    previousMillis = currentMillis;
    BLE.poll();
  }
  
   int16_t accelerometer_X = round(myIMU.readFloatAccelX() * 100.0);
   accelerometerCharacteristic_X.writeValue(accelerometer_X);

}
