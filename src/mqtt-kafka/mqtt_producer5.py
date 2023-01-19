import json
import paho.mqtt.client as mqtt
from random import uniform
import time

mqtt_broker_address = '127.0.0.1'
mqtt_client = mqtt.Client('MQTTProducer')
mqtt_client.connect(mqtt_broker_address)
from datetime import datetime

while True:
        randNumber = uniform(20.0, 21.0)
        timestamp = datetime.now()
        # json으로 encode해서 publish
        mqtt_client.publish("user5", json.dumps({"user": "user5", "timestamp": str(timestamp), "data": randNumber}), 1)
        print('user5_MQTT published : ' + str(timestamp) + ' - ' + str(randNumber))

        time.sleep(4)
