import socket
import threading

HOST = '127.0.0.1'
PORT = 2077

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

stop = False

# Broadcasting
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    global stop
    while not stop:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nickname.remove(nickname)
            client.close
            break

# Receiving
def receive():
    try:
        while True:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            client.send("NICK".encode('utf-8'))
            nickname = client.recv(1024)

            nicknames.append(nickname)
            clients.append(client)

            print(f"Nickname: {nickname}")
            broadcast(f"{nickname} connected to server!\n".encode('utf-8'))
            client.send("Connected to the server".encode('utf-8'))

            thread = threading.Thread(target=handle, args = (client,))
            thread.start()
    except KeyboardInterrupt:
        print("Closing")
        global stop
        stop = True
        return

print(f"Server listening on {HOST}:{PORT}.....")
receive()
