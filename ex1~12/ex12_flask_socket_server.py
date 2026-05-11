# ex12_flask_socket_server.py

# Web server : 웹 페이지를 제공하는 서버 (정적 서비스)
# WAS(Web Application Server) : 웹 애플리케이션을 실행하는 서버 (동적 서비스)


#flask : http 통신, WAS 
# custom_thread: tcpip socket

import socket, threading
from flask import Flask, render_template_string

app = Flask(__name__)
# 센서 데이터 저장 
latest_sensor_data = ""

# ---- tcp socket ----
def start_tcp_server(host, port):
    global latest_sensor_data
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"TCP 소켓 서버 {host}:{port}에서 대기중")
    while True:
        client_socket, address = server_socket.accept()
        print(f"클라이언트 {address} 연결됨")
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                latest_sensor_data = data.decode('utf-8')
                print(f"받은 데이터: {latest_sensor_data}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()


# ---- flask routing ----

@app.route("/")
def home():
    html = f"""
    <html>
    <head></head>
    <body>
    <h1>실시간 센서 값</h1>
    <p>현재 값: {latest_sensor_data}</p>
    <p>[2초마다 자동갱신중]</p>
    <script>setTimeout(function(){{location.reload();}}, 2000)</script>
    </body>
    
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    CLIENT_IP = "163.152.213.114"
    CLIENT_PORT = 9999
    tcp_thread = threading.Thread(target=start_tcp_server, args=(CLIENT_IP, CLIENT_PORT))
    
    tcp_thread.daemon = True
    tcp_thread.start()
    app.run(host="163.152.213.114", port=5000)
    