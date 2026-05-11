#ex1_oneshot_server.py 교재 p21

# 서버 실행 : python ~server.py 8000
# 클라이언트 실행 : python ~client.py 127.0.0.1 8000 

import socket 
import sys 


def main():
    

  
    # step 2 주소설정
    serv_ip = '' #172.30.1.8 이렇게 넣어도 되고, 비워두면 addres any
    serv_port = int(sys.argv[1]) # ex 8000 
    
    # step1 : socket
    serv_sock = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM,
                              0)
    
    try:
        serv_sock.bind((serv_ip,serv_port))
        serv_sock.listen(5)
        print("NOW I am listening ")
        clnt_sock, clnt_addr = serv_sock.accept()
        print(f"connected from: {clnt_addr}")
        message = "hello this is server speaking"
        clnt_sock.send(message.encode('utf-8'))
        clnt_sock.close()
    except Exception as e:
        print(f"error: {e}")
    finally:
        serv_sock.close()
   
    
if __name__ == "__main__":
    main()
    
