import socket

HOST = ('127.0.0.1', 7777)



while 1:
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"    \n----menu----\n\
    1) time\n\
    2) rnd a(int) b(int)\n\
    3) stop\n\
    ")
    command = input("Enter the command: ")
    
    sock.connect(HOST)
    sock.send(command.encode())

    data = sock.recv(1024).decode()

    print(f"\nserver: {data}")

    sock.close()

    if command == "stop":
        print("---stopped---")
        break
    



