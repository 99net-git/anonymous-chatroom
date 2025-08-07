import socket, ssl

server_ip = input("Enter server IP: ")
port = 5555

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

with socket.create_connection((server_ip, port)) as sock:
    with context.wrap_socket(sock, server_hostname=server_ip) as ssock:
        print(ssock.recv(1024).decode(), end='')
        ssock.send(input().encode() + b'\n')
        print(ssock.recv(1024).decode(), end='')
        ssock.send(input().encode() + b'\n')

        def listen():
            while True:
                try:
                    msg = ssock.recv(1024)
                    if msg:
                        print(msg.decode(), end='')
                except:
                    break

        import threading
        threading.Thread(target=listen, daemon=True).start()

        while True:
            try:
                msg = input()
                ssock.send(msg.encode() + b'\n')
            except:
                break
