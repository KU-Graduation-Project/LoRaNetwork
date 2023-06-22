import json
import threading
import time
from datetime import datetime
import websocket

import serial
import struct

import mysql.connector
from kafka import KafkaProducer


# ioLory receiver
# 시리얼포트 연결 설정
def make_port(port_name):
    ser = serial.Serial(
        port=port_name,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=0.05
    )
    ser.isOpen()
    print('receiver open')

    return ser
#ioLory포트
serial_port = make_port('COM4')

# 리액트 소켓주소
Host = '127.0.0.1'
Port = 8080

#리액트와 소켓연결
client_socket = websocket.WebSocket()
client_socket.connect('ws://localhost:8080')

#mysql 연결
conn = mysql.connector.connect(host='localhost',
                               database='oceanlab',
                               user='root',
                               password='12341234')
cur = conn.cursor()


#유저정보 설정확인
isInfoSet = False
# mysql로부터 유저정보 받아와 info_ack 붙임
# 라즈베리파이(중계기)의 uLory에게 송신
# user_info형식 : "info_ack[('1', '01', 'one'), ('2', '02', 'two'), ('5', '05', 'five'), ('6', '06', 'six')]"
def send_user_info():
    global isInfoSet
    if serial_port.readable():
        res = serial_port.readline()
        data = res.decode('utf-8')

        #센서 데이터가 들어오면 유저정보 송신 끝
        #센서 데이터 행위값이 음수
        if "-" in data:
            print("userinfo break:", data)
            isInfoSet = True
        if data == 'info_req':
            print("received:", data)

            cur.execute("SELECT * FROM user")
            user_info = "info_ack" + str(cur.fetchall())
            encoded_user_info = user_info.encode('utf-8')
            print("sent:", encoded_user_info)
            serial_port.write(encoded_user_info)

            '''
            user_info = "info_ack[('1', '01', 'one'), ('2', '02', 'two'), ('5', '05', 'five'), ('6', '06', 'six')]"
            encoded_user_info = user_info.encode()
            print("sent:", encoded_user_info)
            serial_port.write(encoded_user_info)
            '''
            if serial_port.readable():
                res = serial_port.readline()
                data = res.decode()
                print('received:', data)

def receive_data(serial_port):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    if serial_port.readable():
        res = serial_port.readline()
        print("receive data: ", timestamp, " / ", res)
        stream_data(res)
        client_socket.send(res)
    return

#카프카에 유저별(토픽별)로 데이터 publish
#data형식 : tic, did, 배터리, 심박, 체온, 호흡수, ?, 행위, uid, 이름
#           0   1     2     3   4     5   6   7    8    9
def stream_data(data):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    sensor_data = data
    decoded_sensor_data = sensor_data.decode("utf-8")
    strings = decoded_sensor_data.split(",")
    topic = strings[1]  #토픽은 did, kafka에 토픽 생성되어있어야 함
    kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                   value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    kafka_producer.send(topic, decoded_sensor_data)
    print('ioLory in KAFKA out - ' + decoded_sensor_data + ' to ' + topic)


while True:
    if isInfoSet is False:
        send_user_info()
    if isInfoSet is True:
        break


while True:
    print(serial_port.readline())
    receive_data(serial_port)
    time.sleep(0.1)

client_socket.close()