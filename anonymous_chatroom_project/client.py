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
