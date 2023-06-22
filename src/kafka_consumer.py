import json
import multiprocessing
from asyncio.log import logger

#import pymysql
from kafka import KafkaConsumer
#import mysql.connector


'''
conn = mysql.connector.connect(host='localhost',
                               database='oceanlab',
                               user='root',
                               password='12341234')
cur = conn.cursor()
'''

class MessageConsumer:
    topic =""

    def __init__(self, topic):
        # self.conn = mysql.connector.connect(host='localhost',
        #                                database='oceanlab',
        #                                user='root',
        #                                password='12341234')
        # self.cur = conn.cursor()
        self.topic = topic

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
                data = str(message.value.decode("utf-8", "ignore"))

                print(self.topic,': ', data)
                # cur.execute('CREATE TABLE IF NOT EXISTS '+self.topic+'(time text, data text)')
                # self.conn.commit()
                # sql = 'INSERT INTO ' + self.topic + ' (timestamp, g_x) VALUES (\''+timestamp+'\', '+g_x+');'
                # if self.cur.execute(sql):
                #     print(self.topic + " DB save : " + str(m_json))
                # # committing message manually after reading from the topic
                # self.conn.commit()

                consumer.commit()

        except Exception as e:
            print(e)
            logger.exception("failed to create %s", e)

        finally:
            consumer.close()


if __name__ == '__main__':
    device_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    pool = multiprocessing.Pool(processes=10)
    pool.map(MessageConsumer, device_list)

