
//arduino2(v 1.8.19)
#include <ArduinoBLE.h>
#include <LSM6DS3.h>
#include <Wire.h>
 
//IMU 6축 데이터 가져오기 위한 보드객체 생성
LSM6DS3 myIMU(I2C_MODE, 0x6A);    //I2C device address 0x6A


// Characteristic값에 변화가 있을 시 BLE client에게 notifications이 감
BLEService sensorService("f2695042-558b-444e-abca-9203bbff0eca");
BLEUnsignedCharCharacteristic AccXSensorLevel("aae740a7-5cd3-4869-aa09-6d1ec2f89d19", BLERead | BLENotify);
BLEUnsignedCharCharacteristic AccYSensorLevel("401be37e-3922-4631-9b5b-a02648026b6f", BLERead | BLENotify);
BLEUnsignedCharCharacteristic AccZSensorLevel("7a20c2f1-ac8f-4c72-9066-01006cebd51c", BLERead | BLENotify);
BLEUnsignedCharCharacteristic GyroXSensorLevel("c1236163-e6c1-4eba-804e-7ff716c26b54", BLERead | BLENotify);
BLEUnsignedCharCharacteristic GyroYSensorLevel("264c951c-56e8-4c25-8d1e-9e0bbb544e27", BLERead | BLENotify);
BLEUnsignedCharCharacteristic GyroZSensorLevel("fc322974-2280-4352-a81e-2c67995c610a", BLERead | BLENotify);
BLEUnsignedCharCharacteristic TempSensorLevel("81fa899e-a55a-45e3-9dfc-5c92ad4ed8ee", BLERead | BLENotify);


// last sensor data
int oldAccXLevel = 0;
int oldAccYLevel = 0;
float oldAccZLevel = 0;
float oldGyroXLevel = 0;
float oldGyroYLevel = 0;
float oldGyroZLevel = 0;
float oldTempLevel = 0;
long previousMillis = 0;  // last time the sensorlevel was checked, in ms
 
 
void setup()
{
  Serial.begin(9600);
 
  pinMode(LED_BUILTIN, OUTPUT); // initialize the built-in LED pin
  digitalWrite(LED_BUILTIN, HIGH);
  
  // begin initialization
  if (!BLE.begin()) 
  {
    Serial.println("starting BLE failed!");
 
    while (1);
  }
 
  BLE.setLocalName("Seeed");
  BLE.setAdvertisedService(sensorService); // add the service UUID
  sensorService.addCharacteristic(AccXSensorLevel);
  sensorService.addCharacteristic(AccYSensorLevel);
  sensorService.addCharacteristic(AccZSensorLevel);
  sensorService.addCharacteristic(GyroXSensorLevel);
  sensorService.addCharacteristic(GyroYSensorLevel);
  sensorService.addCharacteristic(GyroZSensorLevel);
  sensorService.addCharacteristic(TempSensorLevel);
  BLE.addService(sensorService); // Add the sensorService
  
 
  // start advertising
  BLE.advertise();
 
  Serial.println("Bluetooth® device active, waiting for connections...");
}
 
 
void loop()
{
  // central = BLE로 연결된 기기(스마트폰)
  BLEDevice central = BLE.central();
 
  // if a central is connected to the peripheral:
  if (central)
  {
    Serial.print("Connected to central: ");
    // print the central's BT address:
    Serial.println(central.address());
    // turn on the LED to indicate the connection:
    digitalWrite(LED_BUILTIN, HIGH);
 
    // check the sensor level every 200ms
    // while the central is connected:
    while (central.connected())
    {
      long currentMillis = millis();
      // if 200ms have passed, check the sensor level:
      if (currentMillis - previousMillis >= 200)
      {
        previousMillis = currentMillis;
        updateSensorData();
      }
    }
    // when the central disconnects, turn off the LED:
    digitalWrite(LED_BUILTIN, LOW);
    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
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

  Serial.print("Accelerometer: x=");
  Serial.print(AX, 4);
  Serial.print("/ y=");
  Serial.print(AY, 4);
  Serial.print("/ z=");
  Serial.println(AZ, 4);

  Serial.print("Gyroscope: x=");
  Serial.print(GX, 4);
  Serial.print("/ y=");
  Serial.print(GY, 4);
  Serial.print("/ z=");
  Serial.println(GZ, 4);

  Serial.print("Temperature:");
  Serial.println(Temp);
 
}
