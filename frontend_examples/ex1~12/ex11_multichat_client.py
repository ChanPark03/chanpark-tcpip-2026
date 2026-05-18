# ex11_multichat_client.py

import socket, threading

def receive(client, nickname):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("오류가 발생했거나, 서버와 연결이 끊어짐")
            client.close()
            break


def write(client, nickname):
    while True:
        my_turn = input('')
        client.send(f"{nickname}: {my_turn}".encode('utf-8'))

Host = '163.152.213.114'
Port = 8000

def main():
    nickname = input("닉네임을 입력하세요: ")
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((Host, Port))

    receive_thread = threading.Thread(target=receive, args=(client, nickname))
    receive_thread.start()

    write_thread = threading.Thread(target=write, args=(client, nickname))
    write_thread.start()

if __name__ == "__main__":
    main()