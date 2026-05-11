# ex_oneshot_client.py

import socket, sys

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <IP> <port>")
        sys.exit(1)
    
    serv_ip = sys.argv[1]
    serv_port = int (sys.argv[2])
    
    # step 1: socket()
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM,
                         0)
    try:
        sock.connect((serv_ip, serv_port))
        message_from_server = sock.recv(1024) # 1024: 인터넷 표준 버퍼 사이즈
        if not message_from_server: 
            print("no contents error")
        print(f"Message from server: { \
            message_from_server.decode('utf-8') \
            }")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()
   
if __name__ == "__main__":
    main()