import json
import threading


from pykafka import KafkaClient
import paho.mqtt.client as mqtt
import time

"mqtt 브로커에서 데이터 받아 user별로 카프카에 전달"

#mosquitto연결
mqtt_broker_address = '127.0.0.1'
mqtt_client = mqtt.Client('MQTTConsumer')
mqtt_client.connect(mqtt_broker_address)

kafka_client = KafkaClient(hosts='localhost:9092')


def on_message(client, userdata, message):
    m_decode = str(message.payload.decode("utf-8", "ignore"))
    m_in = json.loads(m_decode)
    topic = m_in["user"]

    kafka_topic = kafka_client.topics[topic]  # 토픽 지정
    kafka_producer = kafka_topic.get_sync_producer()

    msg_payload = str(message.payload)
    print('MQTT message ', msg_payload)
    kafka_producer.produce(str(msg_payload).encode('ascii'))
    print('KAFKA : published ' + str(msg_payload) + 'to ' + topic)


def on_client(mqtt_topic):
    mqtt_client.loop_start()
    print('MQTT Listener open :', mqtt_topic)
    mqtt_client.subscribe(mqtt_topic)  # 토픽 지정
    mqtt_client.on_message = on_message
    time.sleep(400)
    mqtt_client.loop_stop()


"""
if __name__ == '__main__':
    start = time.perf_counter()
    threads = []
    for _ in range(10):
        t = threading.Thread(target=on_client("user"+str(_)))
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()
"""
t1 = threading.Thread(target=on_client("user1"))
t2 = threading.Thread(target=on_client("user2"))
t3 = threading.Thread(target=on_client("user3"))
t4 = threading.Thread(target=on_client("user4"))
t5 = threading.Thread(target=on_client("user5"))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()


