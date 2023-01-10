import paho.mqtt.client as mqtt
from random import uniform
import time

mqtt_broker_address = '127.0.0.1'
mqtt_client = mqtt.Client('MQTTProducer')
mqtt_client.connect(mqtt_broker_address)

while True:
        randNumber = uniform(20.0, 21.0)
        mqtt_client.publish("new-topic", randNumber)
        print('MQTT : Just published' + str(randNumber) + 'to new-topic')

        time.sleep(3)
