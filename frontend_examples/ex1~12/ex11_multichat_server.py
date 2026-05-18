# ex11_multichat_server.py
# 서버는 클라이언트 접속을 관리, 브로드 캐스트(접속한 모두에게 전파)

import socket, threading

Host = '163.152.213.114'
Port = 8000

BROADCAST_COLOR = "\033[96m"  # 밝은 청록색
SYSTEM_COLOR = "\033[93m"     # 노란색
RESET_COLOR = "\033[0m"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((Host, Port))
server.listen()

clients = []
nicknames = []

def color_message(message, color=BROADCAST_COLOR):
    return f"{color}{message}{RESET_COLOR}"


def broadcast(message, color=BROADCAST_COLOR):
    if isinstance(message, bytes):
        message = message.decode('utf-8')

    message = color_message(message, color).encode('utf-8')

    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
            
        
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname}님이 퇴장하였습니다.", SYSTEM_COLOR)
            nicknames.remove(nickname)
            break

def main():
    print("서버가 시작 되었습니다. 연결을 기다립니다 . . .")
    while True:
        client, address = server.accept()
        print(f"연결성공: {str(address)}")
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        
        print(f"사용자 닉네임: {nickname}")
        broadcast(f"{nickname}님이 입장하였습니다.", SYSTEM_COLOR)
        client.send(color_message('서버에 연결 되었습니다.', SYSTEM_COLOR).encode('utf-8'))
        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    main()


