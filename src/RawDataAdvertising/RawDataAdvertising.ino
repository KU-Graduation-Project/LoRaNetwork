#include <ArduinoBLE.h>
#include <LSM6DS3.h>

BLEService myService("fff0");
BLEIntCharacteristic AccXSensorLevel("fff1", BLERead | BLEBroadcast);


//IMU 6축 데이터 가져오기 위한 보드객체 생성
LSM6DS3 myIMU(I2C_MODE, 0x6A);    //I2C device address 0x6A


// Advertising parameters should have a global scope. Do NOT define them in 'setup' or in 'loop'
const uint8_t completeRawAdvertisingData[] = {0x02,0x01,0x06,0x09,0xff,0x01,0x01,0x00,0x01,0x02,0x03,0x04,0x05};   


void setup() {               
//  Serial.begin(9600);
//  while (!Serial);
//
  if (!BLE.begin()){
    //Serial.println("failed to initialize BLE!");
    while (1);
  }

  myService.addCharacteristic(AccXSensorLevel);
  BLE.addService(myService);
  AccXSensorLevel.writeValue(0);
  
  // Build advertising data packet
  BLEAdvertisingData advData;
  // If a packet has a raw data parameter, then all the other parameters of the packet will be ignored
  advData.setRawData(completeRawAdvertisingData, sizeof(completeRawAdvertisingData));  
  // Copy set parameters in the actual advertising packet
  BLE.setAdvertisingData(advData);
  
  // Build scan response data packet
  BLEAdvertisingData scanData;
  scanData.setLocalName("Test advertising raw data");
  // Copy set parameters in the actual scan response packet
  BLE.setScanResponseData(scanData);
  
  BLE.advertise();

//  Serial.println("advertising ...");
}

void loop() {
  
  BLEDevice central = BLE.central();
    
  while (central.connected()){
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);                      
    digitalWrite(LED_BUILTIN, LOW);   
    delay(500);

    //float AX;
    //AX = myIMU.readFloatAccelX();
    //AccXSensorLevel.writeValue(AX);
    
    BLE.poll();
  }
      
}