#include <ArduinoBLE.h>
 
// Bluetooth® Low Energy Battery Service
BLEService batteryService("180F");
 
// Bluetooth® Low Energy Battery Level Characteristic
BLEUnsignedCharCharacteristic batteryLevelChar("2A19", BLERead | BLENotify); // standard 16-bit characteristic UUID
// remote clients will be able to get notifications if this characteristic changes
 
int oldBatteryLevel = 0;  // last battery level reading from analog input
long previousMillis = 0;  // last time the battery level was checked, in ms
 
 
void setup()
{
  Serial.begin(9600);    // initialize serial communication
  while (!Serial);
 
  pinMode(LED_BUILTIN, OUTPUT); // initialize the built-in LED pin to indicate when a central is connected
 
  // begin initialization
  if (!BLE.begin()) 
  {
    Serial.println("starting BLE failed!");
 
    while (1);
  }
 
  BLE.setLocalName("XIAO");
  BLE.setAdvertisedService(batteryService); // add the service UUID
  batteryService.addCharacteristic(batteryLevelChar); // add the battery level characteristic
  BLE.addService(batteryService); // Add the battery service
  batteryLevelChar.writeValue(oldBatteryLevel); // set initial value for this characteristic
 
  // start advertising
  BLE.advertise();
 
  Serial.println("Bluetooth® device active, waiting for connections...");
}
 
 
void loop()
{
  // wait for a Bluetooth® Low Energy central
  BLEDevice central = BLE.central();
 
  // if a central is connected to the peripheral:
  if (central)
  {
    Serial.print("Connected to central: ");
    // print the central's BT address:
    Serial.println(central.address());
    // turn on the LED to indicate the connection:
    digitalWrite(LED_BUILTIN, HIGH);
 
    // check the battery level every 200ms
    // while the central is connected:
    while (central.connected())
    {
      long currentMillis = millis();
      // if 200ms have passed, check the battery level:
      if (currentMillis - previousMillis >= 200)
      {
        previousMillis = currentMillis;
        updateBatteryLevel();
      }
    }
    // when the central disconnects, turn off the LED:
    digitalWrite(LED_BUILTIN, LOW);
    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}
 
void updateBatteryLevel()
{
  /* Read the current voltage level on the A0 analog input pin.
     This is used here to simulate the charge level of a battery.
  */
  int battery = analogRead(A0);
  int batteryLevel = map(battery, 0, 1023, 0, 100);
 
  if (batteryLevel != oldBatteryLevel)    // if the battery level has changed
  { 
    Serial.print("Battery Level % is now: "); // print it
    Serial.println(batteryLevel);
    batteryLevelChar.writeValue(batteryLevel);  // and update the battery level characteristic
    oldBatteryLevel = batteryLevel;           // save the level for next comparison
  }
}
