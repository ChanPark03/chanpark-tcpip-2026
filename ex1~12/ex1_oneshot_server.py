# ex1_oneshot_server.py 교재 P21 (hello.c 를 python으로 다시 작성)

#서버 실행 :  python ~server.py 8000
#클라이언트 실행 : python ~client.py 127.0.0.1 8000
import socket
import sys


def error_handling(message):
    sys.stderr.write(message + "\n")
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <port>")
        sys.exit(1)
        
    #1. socket (21)
    serv_sock = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM,
                              0)
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
        
        
    #4. listen() 
    if serv_sock.listen(5) == -1:
        error_handling("listen() error")
        
    #5. accept()
    try:
        clnt_sock, clnt_addr = serv_sock.accept()
    except socket.error:
        error_handling("accept() error")
        
    #6. write()
    message = "hello this is server speaking"
    clnt_sock.send(message.encode('utf-8'))
    clnt_sock.close()
    serv_sock.close()
    
    # C언어 : ifndef
if __name__ == "__main__":
    main()
