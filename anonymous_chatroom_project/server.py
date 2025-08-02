import socket, ssl, threading, json, bcrypt

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
users_file = "users.json"

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

def load_users():
    with open(users_file, 'r') as f:
        return json.load(f)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    try:
        conn.send("Username: ".encode(FORMAT))
        username = conn.recv(1024).decode(FORMAT)
        conn.send("Password: ".encode(FORMAT))
        password = conn.recv(1024).decode(FORMAT)

        users = load_users()
        if username in users and bcrypt.checkpw(password.encode(), users[username].encode()):
            conn.send("[ACCESS GRANTED] Welcome to Anonymous World!\n".encode(FORMAT))
        else:
            conn.send("[ACCESS DENIED] Invalid credentials.\n".encode(FORMAT))
            conn.close()
            return

        connected = True
        while connected:
            msg = conn.recv(1024)
            if msg:
                print(f"[{username}] {msg.decode(FORMAT)}")
    except:
        pass
    finally:
        conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
print(f"[STARTING] Server is starting on {SERVER}:{PORT}...")

while True:
    client, addr = server.accept()
    conn = context.wrap_socket(client, server_side=True)
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
