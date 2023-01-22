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

# 버퍼 파일 열기
user1 = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/data/user1.txt', 'w')
user2 = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/data/user2.txt', 'w')
user3 = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/data/user3.txt', 'w')
user4 = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/data/user4.txt', 'w')
user5 = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/data/user5.txt', 'w')
user6 = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/data/user6.txt', 'w')
user7 = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/data/user7.txt', 'w')
user8 = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/data/user8.txt', 'w')
user9 = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/data/user9.txt', 'w')
user10 = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/data/user10.txt', 'w')

def on_message(client, userdata, message, file):
    m_decode = str(message.payload.decode("utf-8", "ignore"))
    m_in = json.loads(m_decode)
    topic = m_in["user"]

    msg_payload = str(message.payload)
    print('MQTT message ', msg_payload)
    file.write(msg_payload)


def on_client(mqtt_topic, file):
    mqtt_client.loop_start()
    print('MQTT Listener open :', mqtt_topic)
    mqtt_client.subscribe(mqtt_topic)  # 토픽 지정
    mqtt_client.on_message = on_message
    time.sleep(400)
    mqtt_client.loop_stop()

t1 = threading.Thread(target=on_client("user1", user1))
t2 = threading.Thread(target=on_client("user2", user2))
t3 = threading.Thread(target=on_client("user3", user3))
t4 = threading.Thread(target=on_client("user4", user4))
t5 = threading.Thread(target=on_client("user5", user5))
t6 = threading.Thread(target=on_client("user6", user6))
t7 = threading.Thread(target=on_client("user7", user7))
t8 = threading.Thread(target=on_client("user8", user8))
t9 = threading.Thread(target=on_client("user9", user9))
t10 = threading.Thread(target=on_client("user10", user10))


t1.start()
t1.join()
t2.start()
t2.join()
t3.start()
t3.join()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()
t9.start()
t10.start()
