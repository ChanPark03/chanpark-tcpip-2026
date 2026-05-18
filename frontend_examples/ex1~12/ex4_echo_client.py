
import socket, sys

def error_handling(message):
    sys.stderr.write(message + "\n")
    sys.exit(1)

    
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
    
    while True:
        message = input("Input message(q to quit): ")
        if message.lower() == 'q':
            break
        if not message:
            continue
        sock.sendall(message.encode('utf-8'))
        received_data = sock.recv(1024)
        if not received_data:
            error_handling("socket read() error")
        print(f"Message from server: { received_data.decode('utf-8')}")
    sock.close()
if __name__ == "__main__":
    main()
