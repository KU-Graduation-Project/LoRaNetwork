import socket
import serial
import struct

# uLory sender(COM4/COM6)
# byte_size : data size
def make_port(port_name, baud_rate, byte_size):
    if byte_size == 8:
        bs = serial.EIGHTBITS

    ser = serial.Serial(
        port=port_name,
        baudrate=baud_rate,
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

## Running port
serial_port = make_port('COM4', 9600, 8)

Host = '127.0.0.1'
Port = 9999

#open socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((Host, Port))

server_socket.listen()

#accept client connection
client_socket, addr = server_socket.accept()
print('Connected by ', addr)

while True:
    data = client_socket.recv(2048)
    if not data:
        break
    print('Received from', addr, data.decode())
    #단거리 데이터 받아서 장거리로 보내기
    #if serial_port.write(data) : print("long send succeeded")


client_socket.close()
server_socket.close()

