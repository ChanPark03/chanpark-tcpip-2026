# ex2_oneshot_client_every1byte.py

import socket, sys

def error_handling(message):
    sys.stderr.write(message + '\n')
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
    
    # connect ()
    try:
        sock.connect((serv_ip, serv_port))
    except:
        error_handling("socket connect() error") 
    
    message_buffer = bytearray(30) #배열 30개 
    str_len = 0 
    idx = 0
    while True:
        read_byte = sock.recv(1) # 1Byte 씩 읽기
        if not read_byte:
            break
        message_buffer [idx] = read_byte[0]
        idx+=1 
        str_len+=1
    received_message = message_buffer[:idx].decode('utf-8')
    print(f"Message from server: {received_message}")
    print(f"Function read call count: {str_len}") 
    
        
    sock.close()
if __name__ == "__main__":
    main()