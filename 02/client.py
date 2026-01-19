"""

написать приложение-клиент используя модуль socket работающее в домашней 
локальной сети.
Приложение должно соединятся с сервером по известному адрес:порт и отправлять 
туда текстовые данные.

известно что сервер принимает данные следующего формата:
    "command:reg; login:<login>; password:<pass>" - для регистрации пользователя
    "command:signin; login:<login>; password:<pass>" - для входа пользователя
    
    
с помощью программы зарегистрировать несколько пользователей на сервере и произвести вход


"""

import socket

HOST = ('127.0.0.1', 7777)

while 1:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"    \n----меню----\n\
1) command:reg; login:<login>; password:<pass> - для регистрации пользователя \n\
2) command:signin; login:<login>; password:<pass> - для входа пользователя\n\
3) stop\n\
")

    command = input("Введите команды: ")

    if command =="stop":
            print("---остановка----")
            break

    sock.connect(HOST)
    sock.send(command.encode())
    data = sock.recv(4096).decode()

    print(f"\nсервер: {data}")

    sock.close()

    