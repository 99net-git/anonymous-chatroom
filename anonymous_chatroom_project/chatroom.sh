#!/bin/bash

# Colors
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
NC="\033[0m"

# --------------------
# server.py (embedded)
# --------------------
cat << 'EOF' > server.py
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

EOF

# --------------------
# client.py (embedded)
# --------------------
cat << 'EOF' > client.py
import socket, ssl, os
from colorama import Fore, init
init()

PORT = 5050
FORMAT = 'utf-8'
HEADER = 64
ADDR = (input("Enter Server IP: "), PORT)

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(sock, server_hostname=ADDR[0])
conn.connect(ADDR)

os.system('cls' if os.name == 'nt' else 'clear')
print(Fore.CYAN + """
     _   _                                 _                            
    /_\ | |_   _ _ __ ___   ___  ___  ___| |_ _ __ __ _ _ __   ___ _ __ 
   //_\\| | | | | '_ ` _ \ / _ \/ __|/ _ \ __| '__/ _` | '_ \ / _ \ '__|
  /  _  \ | |_| | | | | | |  __/\__ \  __/ |_| | | (_| | | | |  __/ |   
  \_/ \_/_|\__,_|_| |_| |_|\___||___/\___|\__|_|  \__,_|_| |_|\___|_|   

""" + Fore.RESET)

print(conn.recv(1024).decode(FORMAT))
conn.send(input().encode(FORMAT))
print(conn.recv(1024).decode(FORMAT))
conn.send(input().encode(FORMAT))

response = conn.recv(1024).decode(FORMAT)
print(response)

if "ACCESS GRANTED" in response:
    while True:
        msg = input("You: ")
        conn.send(msg.encode(FORMAT))

EOF

# ------------------------
# add_user.py (disabled)
# ------------------------
cat << 'EOF' > add_user.py
print("User registration is disabled. Only the administrator can create accounts.")

EOF

# ----------------------
# users.json (preloaded)
# ----------------------
cat << 'EOF' > users.json
{
  "@alan": "$2b$12$lmEWhHkchEpzTRFjK3Tj5.vNrxSSaVMBgAEtQyKrTMSJgniW/6Uba",
  "@Zaid": "$2b$12$3kXQAMUOfTCD1LfHGO7JRO7DZQX4IDjlKSEpWGy9CgJkB6syd7Hry",
  "@Blackhat": "$2b$12$l9HGobGmFlHe1iY2R12r/Otf4aY5cZPjAUEDQL0W3kMeFKcAQtE.2",
  "@Ghost": "$2b$12$D4OcZflfdR58aPFxEXXBQ.jZhfzZxSHnKuAm2Ffx3BymvSOEPgRzq"
}

EOF

# ----------------------
# SSL Certificate Generation
# ----------------------
if [ ! -f cert.pem ] || [ ! -f key.pem ]; then
    echo -e "${YELLOW}[*] Generating SSL certificates...${NC}"
    openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
fi

# ----------------------
# Python Requirements
# ----------------------
pip install bcrypt colorama > /dev/null 2>&1

# ----------------------
# Main Menu
# ----------------------
echo -e "${GREEN}Welcome to the Anonymous Chatroom Launcher${NC}"
echo "----------------------------------------"
echo "1. Run Chat Server"
echo "2. Run Chat Client"
echo "3. Add New User (Disabled)"
echo "4. Exit"
echo "----------------------------------------"
read -p "Choose an option (1-4): " choice

case $choice in
    1)
        echo -e "${GREEN}Starting chat server...${NC}"
        python server.py
        ;;
    2)
        echo -e "${GREEN}Starting chat client...${NC}"
        python client.py
        ;;
    3)
        echo -e "${RED}User creation is disabled. Only the admin can add users.${NC}"
        python add_user.py
        ;;
    4)
        echo "Exiting. Bye."
        exit
        ;;
    *)
        echo -e "${RED}Invalid choice. Please run again.${NC}"
        ;;
esac
