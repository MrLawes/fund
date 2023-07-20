import socket
import threading


def forward(src_socket, dest_socket):
    while True:
        data = src_socket.recv(1024)
        if not data:
            break
        dest_socket.sendall(data)
    src_socket.close()
    dest_socket.close()


def handle_client(client_socket, dest_host, dest_port):
    try:
        dest_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest_socket.connect((dest_host, dest_port))
    except Exception as e:
        print(f"Failed to connect to destination server: {e}")
        client_socket.close()
        return

    threading.Thread(target=forward, args=(client_socket, dest_socket)).start()
    threading.Thread(target=forward, args=(dest_socket, client_socket)).start()


def main(local_host, local_port, dest_host, dest_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((local_host, local_port))
    server_socket.listen(5)
    print(f"Listening on {local_host}:{local_port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        threading.Thread(target=handle_client, args=(client_socket, dest_host, dest_port)).start()


if __name__ == "__main__":
    local_host = "127.0.0.1"  # 本地监听地址
    local_port = 80  # 本地监听端口
    dest_host = "127.0.0.1"  # 目标主机地址
    dest_port = 20100  # 目标主机端口
    main(local_host, local_port, dest_host, dest_port)
