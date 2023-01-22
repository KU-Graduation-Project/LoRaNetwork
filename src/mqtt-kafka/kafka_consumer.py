import json
import multiprocessing
from json import dumps

import pymysql
from kafka import KafkaConsumer

"""user# 토픽에서 데이터 받아 db에 저장"""

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
                                    'heartrate int(3), resp int(3), temp int(3))'
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
    while True:
        for message in consumer:
            m_decode = str(message.payload.decode("utf-8", "ignore"))
            m_in = json.loads(m_decode)
            timestamp = m_in["timestamp"]
            g_x = m_in["data"]
            sql = 'INSERT INTO' + topic + '(timestamp, g_x) VALUES (' + timestamp + ', ' + g_x + ');'
            cur.execute(sql)

user_list = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10"]

if __name__=='__main__':
    # 컨슈머 멀티프로세싱
    pool = multiprocessing.Pool(processes=10)
    pool.map(kafka_to_db, user_list)


