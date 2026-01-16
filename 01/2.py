'''
1. написать сервер на сокетах который может принимать 3 команды
    - time - отправляет обратно текущее время
    - rnd a:int b:int - отправляет обратно случайное число от а до b (пример - int 1 6)
    - stop - останавливает сервер - отправляет сообщение об этом
    - если прислана неизвестная  команда сообщить об этом клиенту
    
    * на сервере вести лог всех присланных команд в файл 
    
2. написать клиент который запрашивает бесконечно команду для сервера
    и выводит в консоль ответ.

'''



import socket
from datetime import datetime
import random



HOST=('127.0.0.1',7777)

LOG_FILE = "server.log"
run = True

def time():
    return datetime.now().strftime("%H:%M:%S")

def rnd(a: int, b:int):
    return (f'result: {random.randint(a, b)}')
  

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(HOST)
sock.listen()

print('---start---')

while run:
    print('------listen-------')
    conn, addr = sock.accept()
    print(f'---connected from {addr[0]}---')

    print ('----wait data----')
    data = conn.recv(1024).decode()

    with open(LOG_FILE, "a",encoding="utf-8") as f:
        f.write(f"{datetime.now} | {data}/n")
    
    if data == "time":
        answer = time()

    elif data == "stop":
        answer = "server stopped"
        run = False

    elif data.startswith('rnd'):
        rnd_list = data.split()
        if len(rnd_list) == 3:
            try:
                a = int(rnd_list[1])
                b = int(rnd_list[2])
                answer = rnd(min(a, b), max(a, b))

            except ValueError:
                answer = "variables must be integers"

        else:
            answer = "correct entry - rnd a b"
        
    else:
        answer = "unknown command"
    
    conn.send(answer.encode())
    conn.close()

sock.close()
print('---stopped---')

    
        
    


