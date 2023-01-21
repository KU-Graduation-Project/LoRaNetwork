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


# 파일 열기
f = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/user1.txt', 'w')
f = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/user2.txt', 'w')
f = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/user3.txt', 'w')
f = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/user4.txt', 'w')
f = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/user5.txt', 'w')
f = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/user6.txt', 'w')
f = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/user7.txt', 'w')
f = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/user8.txt', 'w')
f = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/user9.txt', 'w')
f = open('/Users/hyerinmac/Desktop/진행 프로젝트/졸업프로젝트/python folder/motionProject/user10.txt', 'w')

# 파일에 텍스트 쓰기
f.write('blockdmask blog')
f.write('\npython open func')

# 파일 닫기
f.close()
def on_message(client, userdata, message):
    m_decode = str(message.payload.decode("utf-8", "ignore"))
    m_in = json.loads(m_decode)
    topic = m_in["user"]


    msg_payload = str(message.payload)
    print('MQTT message ', msg_payload)


def on_client(mqtt_topic):
    mqtt_client.loop_start()
    print('MQTT Listener open :', mqtt_topic)
    mqtt_client.subscribe(mqtt_topic)  # 토픽 지정
    mqtt_client.on_message = on_message
    time.sleep(400)
    mqtt_client.loop_stop()
