import socket
import threading

HOST = 'localhost'
PORT = 9090

clients = []    # общий список клиентов
nicknames = []  # общий список никнеймов

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} leave chat.".encode('utf-8'))
            break

def main():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(5)

    print("Server started, waiting for connection...")

    while True:
        client, address = sock.accept()
        print(f"Подключен {address}")

        client.send('nickname'.encode('utf-8'))  # запрос никнейма
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Client nickname: {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send("You are connected to the chat!".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    main()
