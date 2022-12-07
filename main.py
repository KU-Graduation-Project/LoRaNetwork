import socket
import argparse
import threading
import time

host = "127.0.0.1"
port = 4000

def handle_client(client_socket, addr):
    print("접속한 클라이언트의 주소 : ", addr)
    user = client_socket.recv(1024)
    string = "%s 님과 소켓 통신 성공"%user.decode()
    client_socket.sendall(string.encode())
    print("1초 후 클라이언트 종료")
    time.sleep(1)
    client_socket.close()

def accept_func():
    global server_socket
    #IPv4 체계 (통신 모뎀 따라 IPv6로 변환 필요할 수도 있음)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #포트의 범위 :  1-65535
    server_socket.bind((host, port))

    #최대 5개 스레드
    server_socket.listen(5)

    while 1:
        try:
            client_socket, addr = server_socket.accept()
        except KeyboardInterrupt:
            server_socket.close()
            print("Keyboard interrupt")

        print("클라이언트 핸들러 스레드로 이동 됩니다.")
        #accept()함수로 입력만 받아주고 이후 알고리즘은 핸들러에게 넘김
        t = threading.Thread(target=handle_client, args=(client_socket, addr))
        t.daemon = True
        t.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="\nServer\n-p port\n")
    parser.add_argument('-p', help="port")

    args = parser.parse_args()
    try:
        port = int(args.p)
    except:
        pass
    accept_func()