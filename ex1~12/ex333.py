import socket
import sys


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <port>")
        sys.exit(1)

    serv_ip = ""
    serv_port = int(sys.argv[1])

    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        serv_sock.bind((serv_ip, serv_port))
        print(f"UDP Server started on port {serv_port}")
        print("클라이언트 메시지를 기다리는 중입니다.")
        print("서버 답장에 q 또는 quit 입력 시 종료됩니다.")

        while True:
            data, clnt_addr = serv_sock.recvfrom(1024)
            message_from_client = data.decode("utf-8")

            print(f"\nClient {clnt_addr}: {message_from_client}")

            if message_from_client.lower() in ("q", "quit"):
                print("클라이언트가 종료 요청을 보냈습니다.")
                break

            message_to_client = input("Server: ")
            serv_sock.sendto(message_to_client.encode("utf-8"), clnt_addr)

            if message_to_client.lower() in ("q", "quit"):
                print("서버를 종료합니다.")
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        serv_sock.close()


if __name__ == "__main__":
    main()
