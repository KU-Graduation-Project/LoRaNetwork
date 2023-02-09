#include <ArduinoBLE.h>
#include <LSM6DS3.h>
#include <Wire.h>

#define CONVERT_TO_MS2    9.80665f
#define MAX_ACCEPTED_RANGE  2.0f

LSM6DS3 myIMU(I2C_MODE, 0x6A);
static bool debug_nn = false;

BLEService myService("fff0");
BLEIntCharacteristic myCharacteristic("fff1", BLERead | BLEBroadcast);

void setup() {
  BLE.begin();
  myIMU.begin();

   BLE.setLocalName("Test sensor");
   myService.addCharacteristic(myCharacteristic);
   BLE.addService(myService);

   BLE.advertise();

}

void loop() {
   BLEDevice central = BLE.central();

   myCharacteristic.writeValue(myIMU.readFloatAccelX());
   BLE.advertise();

}
