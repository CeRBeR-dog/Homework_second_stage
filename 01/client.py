import socket

HOST = ('127.0.0.1', 7777)



while 1:
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    command = input("Enter the command: ")
    
    sock.connect(HOST)
    sock.send(command.encode())

    data = sock.recv(1024).decode()

    print('server: ', data)

    sock.close()

    if command == "stop":
        print("bye")
        break
    



