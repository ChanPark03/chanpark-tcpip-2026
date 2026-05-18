import socket

HOST = '0.0.0.0' 
PORT = 8000

print(f"서버 대기 중... (Port: {PORT})")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    
    conn, addr = s.accept()
    with conn:
        print(f"Pico 2 W 연결됨: {addr}")
        
        while True:
            # 1. Pico로부터 데이터(랜덤 숫자 문자열) 수신
            data = conn.recv(2048)
            if not data:
                break
            
            try:
                # 바이트 데이터를 숫자로 변환
                val_str = data.decode().strip()
                value = float(val_str)
                print(f"수신 데이터: {value}")

                # 2. 조건에 따른 메시지 결정
                if value > 30.0:
                    response = "LED_ON"
                else:
                    response = "LED_OFF"
                
                # 3. Pico로 명령어 전송
                conn.sendall(response.encode())
                print(f"명령 전송: {response}")
                
            except ValueError:
                print(f"잘못된 데이터 수신: {data}")

print("서버 테스트 종료")