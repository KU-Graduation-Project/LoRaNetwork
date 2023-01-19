import json
import threading
from json import dumps

import pymysql
from kafka import KafkaConsumer


def kafka_to_db(topic):
    # DB연결
    conn = pymysql.connect(host='127.0.0.1', user='root', password='password', db='motionDB', charset='utf8')
    cur = conn.cursor()
    sql = 'DROP TABLE IF EXISTS ' + topic
    cur.execute(sql)

    print(topic + ' table created')
    sql = 'CREATE TABLE ' + topic + ' (timestamp datetime, ' \
                                    'g_x decimal(6,3), g_y decimal(6,3), g_z decimal(6,3), ' \
                                    'a_x decimal(6,3), a_y decimal(6,3), a_z decimal(6,3),' \
                                    'heartrate int(3), resp int(3))'
    cur.execute(sql)
    conn.commit()

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='test',
        value_deserializer=lambda x: dumps(x.decode("utf-8")),
        consumer_timeout_ms=1000
    )
    for message in consumer:
        m_decode = str(message.payload.decode("utf-8", "ignore"))
        m_in = json.loads(m_decode)
        timestamp = m_in["timestamp"]
        g_x = m_in["data"]
        sql = 'INSERT INTO' + topic + '(timestamp, g_x) VALUES (' + timestamp + ', ' + g_x + ');'
        cur.execute(sql)


# 컨슈머 멀티스레딩,

t1 = threading.Thread(target=kafka_to_db("user1"))
t2 = threading.Thread(target=kafka_to_db("user2"))
t3 = threading.Thread(target=kafka_to_db("user3"))
t4 = threading.Thread(target=kafka_to_db("user4"))
t5 = threading.Thread(target=kafka_to_db("user5"))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()



