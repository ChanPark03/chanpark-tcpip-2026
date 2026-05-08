import socket, time, random

def main():
    host = "127.0.0.1"
    port = 8000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print("Connected to server")
        for i in range(10):
            current_temp = round(random.uniform(20.0, 40.0), 1) # 20.0 ~ 40.0 사이의 랜덤 온도 생성
            client_socket.send(str(current_temp).encode('utf-8'))
            print(f"현재 온도 전송: {current_temp}°C")
            response = client_socket.recv(1024).decode('utf-8')
            if response == "Motor ON":
                print("[Pico motor on]")
            elif response == "Motor OFF":
                print("[Pico motor off]")
            print("-----------------------------")
            time.sleep(2)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("disconnected")
    
if __name__ == "__main__":
    main()