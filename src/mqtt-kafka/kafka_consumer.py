import json
import multiprocessing
from json import dumps

import pymysql
from kafka import KafkaConsumer

"""user# 토픽에서 데이터 받아 db에 저장"""



class MessageConsumer:
    topic =""

    def __init__(self, topic):
        self.topic = topic
        # DB연결
        conn = pymysql.connect(host='127.0.0.1', user='root', password='password', db='motionDB', charset='utf8')
        cur = conn.cursor()
        sql = 'DROP TABLE IF EXISTS ' + self.topic
        cur.execute(sql)

        print(self.topic + " table created")
        sql = 'CREATE TABLE ' + self.topic + ' (timestamp datetime, ' \
                                             'g_x decimal(6,3), g_y decimal(6,3), g_z decimal(6,3), ' \
                                             'a_x decimal(6,3), a_y decimal(6,3), a_z decimal(6,3),' \
                                             'heartrate int(3), resp int(3), temp int(3))'
        cur.execute(sql)
        conn.commit()

        self.activate_listener()


    def activate_listener(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 group_id='team',
                                 consumer_timeout_ms=60000,
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=False,
                                 #value_deserializer=lambda m: json.loads(m.decode('utf-8'))
                                 )

        consumer.subscribe(self.topic)
        print(self.topic + ": consumer open")
        try:
            for message in consumer:
                m_decode = str(message.value.decode("utf-8", "ignore"))

                print(self.topic + " original m : " + str(message.value))
                print(self.topic + " m_decode : " + m_decode)

                m_in = json.loads(str(m_decode,'utf-8'))
                m_json = json.dumps(m_in)
                timestamp = m_json["timestamp"]
                g_x = m_json["data"]
                sql = 'INSERT INTO' + self.topic + '(timestamp, g_x) VALUES (' + timestamp + ', ' + g_x + ');'
                if self.cur.execute(sql):
                    print(self.topic + " message : " + m_json + " - to db")

                # committing message manually after reading from the topic
                consumer.commit()
        finally:
            consumer.close()


if __name__ == '__main__':
    user_list = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10"]

    pool = multiprocessing.Pool(processes=10)
    pool.map(MessageConsumer, user_list)
    pool.apply()
