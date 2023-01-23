import json
import multiprocessing


from pykafka import KafkaClient
import paho.mqtt.client as mqtt
import time

"mqtt 브로커에서 데이터 받아 user별로 카프카에 전달"


def connect(topic):
    # mosquitto연결
    mqtt_broker_address = '127.0.0.1'
    mqtt_client = mqtt.Client(topic+'_MQTTConsumer')
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

    kafka_client = KafkaClient(hosts='localhost:9092')
    kafka_topic = kafka_client.topics[topic]  # 토픽 지정
    kafka_producer = kafka_topic.get_sync_producer()

    msg_payload = str(message.payload)
    print('MQTT in - ', msg_payload)
    kafka_producer.produce(str(msg_payload).encode('ascii'))
    print('KAFKA out - ' + str(msg_payload) + ' to ' + topic)


user_list = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10"]


if __name__=='__main__':
    # 컨슈머 멀티프로세싱
    pool = multiprocessing.Pool(processes=3)
    pool.map(connect, user_list)


