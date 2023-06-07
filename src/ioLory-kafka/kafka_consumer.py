import json
import multiprocessing
from asyncio.log import logger

#import pymysql
from kafka import KafkaConsumer
import socket

"""토픽에서 데이터 받아 리액트로 소켓 전송"""


# open socket client
# send data to web
Host = '127.0.0.1'
Port = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((Host, Port))


class MessageConsumer:
    topic =""

    def __init__(self, topic):
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
                m_decode = str(message.value.decode("utf-8", "ignore"))
                m_in = m_decode[:len(m_decode)]
                client_socket.sendall(m_in)

                # m_json = json.loads(m_in)
                # timestamp = m_json["timestamp"]
                # g_x = str(m_json["data"])
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

