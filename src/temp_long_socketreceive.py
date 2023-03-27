import socket

# receive data through socket

Host = '127.0.0.1'
Port = 9998

#open socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((Host, Port))
print('socket server open')

server_socket.listen()

#accept client connection
client_socket, addr = server_socket.accept()
print('Connected by ', addr)

while True:
    data = client_socket.recv(2048)
    if not data:
        break
    print('Received from', addr, data.decode())
    #장거리 데이터 받아서 리액트로 보내주기


client_socket.close()
server_socket.close()

