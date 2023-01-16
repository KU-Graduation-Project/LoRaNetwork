import time
import serial
import numpy as np
import threading
import struct

# portName : COM4, rate : baundrate other side of rate,
# byte_size : data size
def make_port(port_name, rate, byte_size):
    if byte_size == 8:
        bs = serial.EIGHTBITS

    ser = serial.Serial(
        port=port_name,
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize= serial.EIGHTBITS
    )

    ser.isOpen()

    return ser

def send_data(datalist, serial_port) :
    if serial_port.isOpen() :
        for data in datalist :
            serial_port.write(data)

#draw graph main 참고 하여 import 후 작성
def draw_graph(a) :
    print("graph"+a)
    return


## Running part
serial_port = make_port('COM4', 9600, 8)

#Make Data

#send_data
while True :
    y = 0.755
    i = 1
    c = 'e'
    bi = i.to_bytes(4, 'big')
    by = struct.pack('f', y)
    bc = bytes(c, 'utf-8')
    data = [bi, by, bc]
    send_data(data, serial_port)



receiving_thread = threading.Thread(target=receive_data, args=(serial_port, arr))
# receiving_thread = threading.Thread(target=draw_graph, args=(5,))
receiving_thread.start()
threading.Timer(1, receive_data, [serial_port, arr])

while True :
    time.sleep(5)