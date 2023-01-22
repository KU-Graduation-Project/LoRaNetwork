import json
import multiprocessing

import paho.mqtt.client as mqtt
from random import uniform
import time
from datetime import datetime

mqtt_broker_address = '127.0.0.1'
mqtt_client = mqtt.Client('MQTTProducer')
mqtt_client.connect(mqtt_broker_address)

def make_producer(user) :
    while True :
        randNumber = uniform(20.0, 21.0)
        timestamp = datetime.now()
        # json으로 encode해서 publish
        mqtt_client.publish(user, json.dumps({"user": user, "timestamp": str(timestamp), "data": randNumber}), 1)
        print(user+'_MQTT published : ' + str(timestamp) +' - ' + str(randNumber))

        time.sleep(4)

user_list = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10"]

if __name__=='__main__':
    # 컨슈머 멀티프로세싱
    pool = multiprocessing.Pool(processes=10)
    pool.map(make_producer, user_list)
