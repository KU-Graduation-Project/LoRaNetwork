import random
import string
import threading
import serial
import time
import pandas as pd
import struct
from queue import Queue


class lora :
    port_name = "port_name"

    def __init__(self, port_name):
        lora.port_name = port_name
        # self.ser = self.__make_port(port_name)

    #Making serial port
    #port_name : Using port name
    def __make_port(self, port_name):
        ser = serial.Serial(
            port=port_name,
            baudrate=9600,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize= serial.EIGHTBITS
        )

        ser.isOpen()

        return ser

    #Receiving Data, Thread 1, this function read byte data from serial port and save in datalist
    #ser : serial port
    #datalist : global memory for sharing data with other threads
    def receive(self, period, datalist_len, datalist_queue) :
        threading.Timer(period, self.receive, [self.ser, datalist_len, datalist_queue, ]).start()

        if self.ser.readable() > 0:
            receive_data = []
            for i in range(datalist_len) :
                receive_data.append(self.ser.read())

        datalist_queue.append(receive_data)
        datalist_queue.put(receive_data)
        return

    def ex_receive(self, period, datalist_len, datalist_queue):
        threading.Timer(period, self.ex_receive, [period, datalist_len, datalist_queue, ]).start()
        x1 = random.randint(0,50).to_bytes(4, "big")
        x2 = struct.pack('f', random.uniform(35, 37))
        x3 = bytes(random.choice(string.ascii_letters), 'utf-8')
        datalist_queue.put([x1, x2, x3])
        return

    def byte_to_datatype(self, data, datatype):

        match datatype:
            case 'int':
                return int.from_bytes(data, "big")
            case 'float':
                return struct.unpack('f', data)
            case 'char':
                return data.decode("utf-8")
        return

    def datatype_to_byte(self, data, datatype):
        match datatype:
            case 'int':
                return data.to_bytes(4, 'big')
            case 'float':
                return struct.pack('f', data)
            case 'char':
                return bytes(data, 'utf-8')
        return


    def send(self, period, datalist_queue):
        # threading.Timer(period, self.send, [self.ser, period, datalist_queue]).start()
        #because arguement error because of queue
        threading.Timer(period, self.send, [self.ser, period, datalist_queue,]).start()

        perioid = period*1000

        if self.ser.isOpen():
            if datalist_queue.empty() == False :
                datalist_queue.task_done()
                datalist = datalist_queue.get()
                for data in datalist :
                    self.ser.write(data)
                self.ser.write(data)


    def ex_send(self, period, send_data):
        threading.Timer(period, self.ex_send, [period, send_data, ]).start()

        if send_data.empty() == False:
            send_data.task_done()
            datalist = send_data.get()
            for data in datalist:
                print(data)
        else:
            print("0")
        return