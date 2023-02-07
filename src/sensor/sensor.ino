
//arduino2(v 1.8.19)
#include <ArduinoBLE.h>
#include <LSM6DS3.h>
#include <Wire.h>


// Characteristic값에 변화가 있을 시 BLE client에게 notifications이 감
BLEService bleService("fff0");
//DeviceInformation("180A")
BLEUnsignedCharCharacteristic AccXSensorLevel("aae740a7-5cd3-4869-aa09-6d1ec2f89d19", BLERead | BLEWrite | BLENotify);
BLEUnsignedCharCharacteristic AccYSensorLevel("401be37e-3922-4631-9b5b-a02648026b6f", BLERead | BLEWrite | BLENotify);
BLEUnsignedCharCharacteristic AccZSensorLevel("7a20c2f1-ac8f-4c72-9066-01006cebd51c", BLERead | BLEWrite | BLENotify);
BLEUnsignedCharCharacteristic GyroXSensorLevel("c1236163-e6c1-4eba-804e-7ff716c26b54", BLERead | BLEWrite | BLENotify);
BLEUnsignedCharCharacteristic GyroYSensorLevel("264c951c-56e8-4c25-8d1e-9e0bbb544e27", BLERead | BLEWrite | BLENotify);
BLEUnsignedCharCharacteristic GyroZSensorLevel("fc322974-2280-4352-a81e-2c67995c610a", BLERead | BLEWrite | BLENotify);
BLEUnsignedCharCharacteristic TempSensorLevel("81fa899e-a55a-45e3-9dfc-5c92ad4ed8ee", BLERead | BLEWrite | BLENotify);

const int ledPin = LED_BUILTIN;

// last sensor data
float oldAccXLevel = 0;
float oldAccYLevel = 0;
float oldAccZLevel = 0;
float oldGyroXLevel = 0;
float oldGyroYLevel = 0;
float oldGyroZLevel = 0;
float oldTempLevel = 0;
long previousMillis = 0;  // last time the sensorlevel was checked, in ms

//IMU 6축 데이터 가져오기 위한 보드객체 생성
LSM6DS3 myIMU(I2C_MODE, 0x6A);    //I2C device address 0x6A
 
void setup(){
  
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
  
  BLE.setLocalName("Seeed");
  BLE.setAdvertisedService(bleService); // add the service UUID
  bleService.addCharacteristic(AccXSensorLevel);
  bleService.addCharacteristic(AccYSensorLevel);
  bleService.addCharacteristic(AccZSensorLevel);
  bleService.addCharacteristic(GyroXSensorLevel);
  bleService.addCharacteristic(GyroYSensorLevel);
  bleService.addCharacteristic(GyroZSensorLevel);
  bleService.addCharacteristic(TempSensorLevel);
  BLE.addService(bleService); // Add the bleService

  AccXSensorLevel.writeValue(0);
  AccYSensorLevel.writeValue(0);
  AccZSensorLevel.writeValue(0);
  GyroXSensorLevel.writeValue(0);
  GyroYSensorLevel.writeValue(0);
  GyroZSensorLevel.writeValue(0);
  TempSensorLevel.writeValue(0);
 
  // start advertising
  BLE.advertise();
}
 
 
void loop(){
  
  // central = BLE로 연결한 기기(스마트폰)
  BLEDevice central = BLE.central();

  // if a central(스마트폰) is connected to the peripheral(Xiao기기)
  if (central){
    //Serial.print("Connected to central: ");
    //Serial.println(central.address());
 
    while (central.connected())
    {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);                      
      digitalWrite(LED_BUILTIN, LOW);   
      delay(500); 
      long currentMillis = millis();
      if (currentMillis - previousMillis >= 200)
      {
        previousMillis = currentMillis;
        updateSensorData();
      }
    }
    
    //digitalWrite(LED_BUILTIN, LOW);
//    Serial.print("Disconnected from central: ");
//    Serial.println(central.address());
  }
}
 

void updateSensorData()
{
  float AX, AY, AZ;
  AX = myIMU.readFloatAccelX();
  AY = myIMU.readFloatAccelY();
  AZ = myIMU.readFloatAccelZ();

  float GX, GY, GZ;
  GX = myIMU.readFloatGyroX();
  GY = myIMU.readFloatGyroY();
  GZ = myIMU.readFloatGyroZ();

  float Temp;
  Temp = myIMU.readTempC();
  
  if (AX != oldAccXLevel) {
  AccXSensorLevel.writeValue(AX);
  oldAccXLevel = AX;
  }

  if (AY != oldAccYLevel) {
  AccYSensorLevel.writeValue(AY);
  oldAccYLevel = AY;
  }

  if (AZ != oldAccZLevel) {
  AccZSensorLevel.writeValue(AZ);
  oldAccZLevel = AZ;
  }

  if (GX != oldGyroXLevel) {
  GyroXSensorLevel.writeValue(GX);
  oldGyroXLevel = GX;
  }

  if (GY != oldGyroYLevel) {
  GyroYSensorLevel.writeValue(GY);
  oldGyroYLevel = GY;
  }

  if (GZ != oldGyroZLevel) {
  GyroZSensorLevel.writeValue(GZ);
  oldGyroZLevel = GZ;
  }

  if (Temp != oldTempLevel) {
  TempSensorLevel.writeValue(Temp);
  oldTempLevel = Temp;
  }

//  Serial.print("Accelerometer: x=");
//  Serial.print(AX, 4);
//  Serial.print("/ y=");
//  Serial.print(AY, 4);
//  Serial.print("/ z=");
//  Serial.println(AZ, 4);

}
