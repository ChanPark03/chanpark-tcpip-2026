import socket, sys 
def main():
    # 1. SOCK_DGRAM(UDP) 소켓 생성
    serv_sock = socket.socket(socket.AF_INET,
                              socket.SOCK_DGRAM)
    # 2. binding
    serv_sock.bind(("", 8001))
    print("UDP Server started on port 8001")
    
    # 3. 클라이언트 접속 대기 
    data, addr = serv_sock.recvfrom(1024)
    print(f"Signal received from {addr}")
    
    # 4. 데이터 전송
    message = "Hello world"
    serv_sock.sendto(message.encode('utf-8'), addr)
    print("Message sent via UDP")
    
    serv_sock.close()
    
if __name__ == "__main__":
    main()