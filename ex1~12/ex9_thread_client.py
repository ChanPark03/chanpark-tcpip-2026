import socket, threading, sys

def send_msg(sock):
    while True:
        message = input("Input message(q to quit): ")
        if message.lower() == 'q':
            break
        if not message:
            continue
        sock.sendall(message.encode('utf-8'))
    try:
        sock.shutdown(socket.SHUT_WR)
    except socket.error:
        pass

def recv_msg(sock):
    while True:
        try:
            received_data = sock.recv(1024)
            if not received_data:
                print("server disconnected")
                break
            print(f"Message from server: { received_data.decode('utf-8')}")
        except socket.error:
            print("socket read() error")
            break
    
def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} <IP> <port>")
        sys.exit(1)
        
    #1. socket (21)
    sock = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM,
                              0)
  
        
    serv_ip = sys.argv[1]
    serv_port = int(sys.argv[2]) 
    
    try:
        sock.connect((serv_ip, serv_port))
    except:
        print("socket connect() error")
        return

    snd = threading.Thread(target=send_msg, args=(sock,))
    rcv = threading.Thread(target=recv_msg, args=(sock,))
    snd.start()
    rcv.start()
    snd.join()
    print("send thread terminated")
    rcv.join()
    print("recv thread terminated")
    sock.close()
    
    
        
if __name__ == "__main__":
    main()
