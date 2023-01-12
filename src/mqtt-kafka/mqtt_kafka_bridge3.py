from pykafka import KafkaClient
import paho.mqtt.client as mqtt
import time

mqtt_broker_address = '127.0.0.1'
mqtt_client = mqtt.Client('MQTTConsumer')
mqtt_client.connect(mqtt_broker_address)

kafka_client = KafkaClient(hosts='localhost:9092')
kafka_topic = kafka_client.topics['test3'] #토픽 지정
kafka_producer = kafka_topic.get_sync_producer()

def on_message(client, userdata, message):
    msg_payload = str(message.payload)
    print('Received test3_MQTT message', msg_payload)
    kafka_producer.produce(str(msg_payload).encode('ascii'))
    print('test3_KAFKA : published' + str(msg_payload) + 'to test3')

mqtt_client.loop_start()
mqtt_client.subscribe('test3') #토픽 지정
mqtt_client.on_message = on_message
time.sleep(300)
mqtt_client.loop_stop()