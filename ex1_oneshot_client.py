# ex_oneshot_client.py

import socket, sys


    
def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <IP> <port>")
        sys.exit(1)
    # step 1: socket()
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM,
                         0)
    if sock.fileno() == -1:
        error_handling("socket connect() error")
    # 서버 주소 설정 
    serv_ip = sys.argv[1]
    serv_port = int (sys.argv[2])
    
    # connect 
    try:
        sock.connect((serv_ip, serv_port))
    except:
        error_handling("socket connect() error") 
    
    # step 4 : read()
    try:
        message_from_server = sock.recv(30) # 30: 버퍼 사이즈 
        if not message_from_server: 
            error_handling("no contents error")
        print(f"Message from server: { \
            message_from_server.decode('utf-8') \
            }")
    except socket.error:
        error_handling("read() error")
    sock.close()
if __name__ == "__main__":
    main()