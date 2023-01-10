import time
from random import uniform
from pykafka import KafkaClient
import paho.mqtt.client as mqtt

mqtt_broker_address = '127.0.0.1'
mqtt_client = mqtt.Client('MQTTProducer')
mqtt_client.connect(mqtt_broker_address)

kafka_client = KafkaClient(hosts='localhost:9092')
kafka_topic = kafka_client.topics['new-topic'] #토픽 지정
kafka_producer = kafka_topic.get_sync_producer()

while True:
        randNumber = uniform(20.0, 21.0)
        mqtt_client.publish("new-topic", randNumber)
        print('MQTT : Just published' + str(randNumber) + 'to new-topic')

        kafka_producer.produce(str(randNumber).encode('ascii'))
        print('KAFKA : Just published' + str(randNumber) + 'to new-topic')
        time.sleep(3)


