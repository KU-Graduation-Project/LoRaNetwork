import multiprocessing
import threading
import time
from datetime import datetime

import serial
import struct


# ioLory receiver(COM5)
# Making serial port
# port_name : Using port name
def make_port(port_name):
    ser = serial.Serial(
        port=port_name,
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    ser.isOpen()
    print('receiver open')

    return ser


# Receiving Data, Thread 1, this function read byte data from serial port and save in datalist
# ser : serial port
# datalist : global memory for sharing data with other threads


class ioLoryReceiver:

    def __int__(self):
        # Running Port
        serial_port = make_port('COM5')

        while True:
            # ser.write(b'check serial data')
            # print(serial_port.readline())
            self.receive_data(serial_port)
            time.sleep(0.1)

    def receive_data(serial_port):
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
        if serial_port.readable():
            res = serial_port.read()
            print("receive data: ", timestamp, " / ", res)
        return

    '''
    def save_data(data, byte_data):
        intData = int.from_bytes(byte_data[0], "big")
        floatData = struct.unpack('f', byte_data[1])
        charData = byte_data[2].decode("utf-8")
        new_data = {
            'intData': intData,
            'floatData': floatData[0],
            'charData': charData
        }

        data = data.append(new_data, ignore_index=True)
        threading.Timer(1, save_data, [data, byte_data]).start()
        # print(data)
        return data
    '''


if __name__ == '__main__':
    user_list = ["user1", "user2", "user3", "user4", "user5", "user6", "user7", "user8", "user9", "user10"]

    pool = multiprocessing.Pool(processes=10)
    pool.map(ioLoryReceiver, user_list)

