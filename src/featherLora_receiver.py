import json
import threading
import time
from datetime import datetime, time as tm
import socket

import serial
import struct
import sqlite3
import numpy as np

# feather M0 LoRa receiver
# feather M0 transmitter로부터 데이터 받아 db에 저장/uLory에 소켓전송
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

# Running Port
serial_port = make_port('/dev/ttyACM0')

#소켓 클라이언트
Host = '127.0.0.1'
Port = 9999
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((Host, Port))

#sqlite DB 연결
conn = sqlite3.connect("////home/pi/Downloads/marin/src/oceanlab")
# if no sensordata.db make sensordata.db
global cur
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS sensor_data(ID INTEGER PRIMARY KEY AUTOINCREMENT, data text)')
cur.execute('DELETE FROM sensor_data')
cur.execute('CREATE TABLE IF NOT EXISTS time(uid int, timestamp text, tic int)')
cur.execute('DELETE FROM time')
cur.execute('CREATE TABLE IF NOT EXISTS user(did text primary key, uid text, name text)')
cur.execute('DELETE FROM user')
conn.commit()

arr = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
#기기별 틱 정보가 저장됐는지 확인하기 위한 배열
ticArr = np.array(arr, dtype='bool')

def receive_data(serial_port):
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    if serial_port.readable():
        data = serial_port.readline()[:-4]  #remove '/r/n'
        print("receive data: ", timestamp, " / ", data)
        save_data(data)
    return

def save_data(bytedata):
    data = bytedata.decode('utf-8')
    
    if(len(data)>4):
        null_data = None
        strings = data.split(',', 2)
        did = strings[1]
        tic = strings[0]
        
        cur.execute("SELECT uid FROM user WHERE did = '%s'" % did)
        uid = ""
        result = cur.fetchone()
        if result is not None :
            uid = str(result)[2:-3]
            uidIdx = int(uid)
            #연결 후 첫 틱 저장
            if ticArr[uidIdx] is False:
                nowTime = datetime.now()
                nowTimestamp = nowTime.strftime('%Y-%m-%d %H:%M:%S')
                cur.execute("INSERT INTO time VALUES(?,?,?)", (uid, nowTimestamp, tic))
                conn.commit()
                ticArr[uidIdx] = True

        #DB에서 유저 이름 찾아서 데이터 마지막에 추가
        data = data +","+ uid
        cur.execute("SELECT name FROM user WHERE did = '%s'" % did)
        name = str(cur.fetchall())[3:-4]
        data = data +","+ name
        
        client_socket.sendall(data.encode('utf-8'))
        cur.execute("INSERT INTO sensor_data VALUES(?,?)", (null_data, data))
        conn.commit()
        

while True:
    receive_data(serial_port)
    time.sleep(0.1)

client_socket.close()

