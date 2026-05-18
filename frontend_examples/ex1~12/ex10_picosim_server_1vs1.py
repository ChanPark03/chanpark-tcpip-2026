import socket 
def main():
    host = '127.0.0.1'  
    port = 8000
    threshold = 30.0 # 모터 제어 경계 온도
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server started")
    conn, addr = server_socket.accept()
    print(f"clinet {addr} is connected")
    try:
        while True: 
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            temp = float(data)
            print(f"수신 온도: {temp}")
            if temp > threshold:
                response = "Motor ON"
            else:
                response = "Motor OFF"
            conn.send(response.encode('utf-8'))
            print(f"제어명령 전송: {response}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        server_socket.close()
if __name__ == "__main__":
    main()