import socket
import serial
import struct
import sqlite3
import time

# uLory sender(COM4/COM6)
# byte_size : data size
def make_port(port_name):
    ser = serial.Serial(
        port=port_name,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=0.5
    )

    ser.isOpen()
    print('sender port open')

    return ser

def send_data(data):
    serial_port.write(data)


# Running Port
serial_port = make_port('/dev/ttyUSB0')
conn = sqlite3.connect("////home/pi/Downloads/marin/src/oceanlab")
global cur
cur = conn.cursor()



while True:
    cur.execute("SELECT COUNT(data) FROM sensor_data")
    st = str(cur.fetchall())[2:-3]
    datasize = int(st)
    if(datasize>=4):
        cur.execute("SELECT data FROM sensor_data")
        data = bytearray(str(cur.fetchall())[2:-1], encoding='utf-8')
        if serial_port.write(data) : print("sned: ",data)
        cur.execute("DELETE FROM sensor_data")
        conn.commit()
    time.sleep(0.5)


