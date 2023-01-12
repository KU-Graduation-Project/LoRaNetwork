import json
import paho.mqtt.client as mqtt
from random import uniform
import time

mqtt_broker_address = '127.0.0.1'
mqtt_client = mqtt.Client('MQTTProducer')
mqtt_client.connect(mqtt_broker_address)

while True:
        randNumber = uniform(20.0, 21.0)
        # json으로 encode해서 publish
        mqtt_client.publish("test2", json.dumps({"user": "test4", "data": randNumber}), 1)
        print('test4_MQTT : published ' + str(randNumber))

        time.sleep(4)
