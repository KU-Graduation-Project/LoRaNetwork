import time
from datetime import datetime
from kafka import KafkaProducer, KafkaClient, KafkaConsumer
import json


# 카프카에 유저별(토픽별)로 데이터 publish
# 카프카에 유저별(토픽별)로 데이터 publish
# data형식 : tic, did, 배터리, 심박, 체온, 호흡수, ?, 행위, uid, 이름
#           0   1     2     3   4     5   6   7    8    9
def stream_data(data):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    sensor_data = data
    decoded_sensor_data = sensor_data.decode("utf-8")
    strings = decoded_sensor_data.split(",")
    topic = strings[1] #토픽은 did
    print('kafka topic:',topic)
    kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                   value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    #client = KafkaClient(bootstrap_servers='localhost:9092')
    #client.ensure_topic_exists(topic)

    kafka_producer.send(topic, decoded_sensor_data)
    print(timestamp+' ioLory in KAFKA out - ' + decoded_sensor_data + ' to ' + topic)
    time.sleep(1)


while True:
    string_data = "2315,1,52,82,65,48,49,-2,01,one"
    print('kafka publish')
    data = string_data.encode("utf-8")
    stream_data(data)
