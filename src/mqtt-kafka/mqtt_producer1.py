import json
import paho.mqtt.client as mqtt
from random import uniform
import time
from datetime import datetime

mqtt_broker_address = '127.0.0.1'
mqtt_client = mqtt.Client('MQTTProducer')
mqtt_client.connect(mqtt_broker_address)

while True:
    randNumber = uniform(20.0, 21.0)
    timestamp = datetime.now()
    # json으로 encode해서 publish
    mqtt_client.publish("user1", json.dumps({"user": "user1", "timestamp": str(timestamp), "data": randNumber}), 1)
    print('user1_MQTT published : ' + str(timestamp) +' - ' + str(randNumber))

    time.sleep(4)
