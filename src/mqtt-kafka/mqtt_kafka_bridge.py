import json
import multiprocessing

from kafka import KafkaProducer
import paho.mqtt.client as mqtt
import time

"mqtt 브로커에서 데이터 받아 user별로 카프카에 전달"


def connect(topic):
    # mosquitto연결
    mqtt_broker_address = '127.0.0.1'
    mqtt_client = mqtt.Client(topic + '_MQTTConsumer')
    mqtt_client.connect(mqtt_broker_address)
    mqtt_topic = topic

    if mqtt_client.subscribe(mqtt_topic):
        print('MQTT Listener open :' + mqtt_topic)
    mqtt_client.on_message = on_message
    mqtt_client.loop_forever()


def on_message(client, userdata, message):
    m_decode = str(message.payload.decode("utf-8", "ignore"))
    m_in = json.loads(m_decode)
    topic = m_in["user"]

    kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                   value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    print('MQTT in - ', message.payload)
    kafka_producer.send(topic, m_in)
    print('KAFKA out - ' + str(json.dumps(m_in).encode('utf-8')) + ' to ' + topic)


user_list = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10"]


if __name__ == '__main__':
    # 컨슈머 멀티프로세싱
    pool = multiprocessing.Pool(processes=10)
    pool.map(connect, user_list)
