import socket
import ssl
import threading
import json
import bcrypt

# Load users
with open("users.json", "r") as f:
    users = json.load(f)

# Server setup
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12345

clients = []

def broadcast(message, conn):
    for client in clients:
        if client != conn:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")

    # Authentication
    conn.send(b"Username: ")
    username = conn.recv(1024).decode().strip()
    conn.send(b"Password: ")
    password = conn.recv(1024).decode().strip()

    if username not in users or not bcrypt.checkpw(password.encode(), users[username].encode()):
        conn.send(b"Authentication failed. Connection closed.\n")
        conn.close()
        return

    conn.send(b"Welcome to the Anonymous Chatroom!\n")
    clients.append(conn)

    while True:
        try:
            msg = conn.recv(1024)
            if not msg:
                break
            broadcast(f"{username}: {msg.decode()}".encode(), conn)
        except:
            break

    conn.close()
    clients.remove(conn)
    print(f"[-] {addr} disconnected")

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"[+] Server listening on port {PORT}")

while True:
    conn, addr = server.accept()
    conn = context.wrap_socket(conn, server_side=True)
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
