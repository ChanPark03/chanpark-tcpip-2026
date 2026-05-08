import socket, multiprocessing, os, sys

def error_handling(message):
    sys.stderr.write(message + "\n")
    sys.exit(1)
    
def handle_client(clnt_sock, addr):
    print(f"child process handling client: {addr}")
    try:
        while True:
            data = clnt_sock.recv(1024)
            if not data:
                break
            clnt_sock.sendall(data)
    finally:
        clnt_sock.close()
        print(f"client {addr} is disconnected..")
     
def main():   
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <port>")
        sys.exit(1)
        
    #1. socket (21)
    serv_sock = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM,
                              0)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if serv_sock.fileno() == -1:
        error_handling("socket() error")
    
    #2. 주소 설정
    #172.30.1.8 이렇게 넣어도 되고, 비워 두면 address any
    
    serv_ip = '' 
    serv_port = int(sys.argv[1]) # ex 8000
    
    #3. 초기화
    try:
        serv_sock.bind((serv_ip,serv_port))
    except socket.error:
        error_handling("bind() error")
    serv_sock.settimeout(1.0)
    serv_sock.listen(2)
    print("Multi-process server started!")
    
    while True:
        try:
            try:
                clnt_sock, clnt_addr = serv_sock.accept()
                print("new client connectd")
            except socket.timeout:
                continue
        except KeyboardInterrupt:
            break
        
        # fork()
        p = multiprocessing.Process(target=handle_client, args=(clnt_sock, clnt_addr))
        
        p.start()
        clnt_sock.close()
        
    serv_sock.close()
if __name__ == "__main__":
    main()
