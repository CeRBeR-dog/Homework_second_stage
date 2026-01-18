'''
написать приложение-сервер используя модуль socket работающее в домашней 
локальной сети.
Приложение должно принимать данные с любого устройства в сети отправленные 
или через программу клиент или через браузер
    - если данные пришли по протоколу http создать возможность след.логики:
        - если путь "/" - вывести главную страницу
        
        - если путь содержит /test/<int>/ вывести сообщение - тест с номером int запущен
                пример - 127.0.0.1:7777/test/1/
        
        - если путь содержит message/<login>/<text>/ вывести в консоль/браузер сообщение
            "{дата время} - сообщение от пользователя {login} - {text}"
        
        - если путь содержит указание на файл вывести в браузер этот файл
        
        - во всех остальных случаях вывести сообщение:
            "пришли неизвестные  данные по HTTP - путь такой то"
                   
         
    - если данные пришли НЕ по протоколу http создать возможность след.логики:
        - если пришла строка формата "command:reg; login:<login>; password:<pass>"
            - выполнить проверку:
                login - только латинские символы и цифры, минимум 6 символов
                password - минимум 8 символов, должны быть хоть 1 цифра
            - при успешной проверке:
                1. вывести сообщение на стороне клиента: 
                    "{дата время} - пользователь {login} зарегистрирован"
                2. добавить данные пользователя в список/словарь на сервере
            - если проверка не прошла вывести сообщение на стороне клиента:
                "{дата время} - ошибка регистрации {login} - неверный пароль/логин"
                
        - если пришла строка формата "command:signin; login:<login>; password:<pass>"
            выполнить проверку зарегистрирован ли такой пользователь на сервере:                
            
            при успешной проверке:
                1. вывести сообщение на стороне клиента: 
                    "{дата время} - пользователь {login} произведен вход"
                
            если проверка не прошла вывести сообщение на стороне клиента:
                "{дата время} - ошибка входа {login} - неверный пароль/логин"
        
        - во всех остальных случаях вывести сообщение на стороне клиента:
            "пришли неизвестные  данные - <присланные данные>"       
                 

'''


import socket
from datetime import datetime

def send_file(file_name,conn):
    try:
        with open(file_name.lstrip('/'), 'rb') as f:
            print(f"send file {file_name}")
            conn.send(OK)
            conn.send(HEADERS)
            conn.send(f.read())
    
    except IOError:
        print('no file')
        conn.send(ERR_404)

def is_file(path):
    if '.' in path:
        ext = path.split(".")[-1]
        if ext in ['jpg','png','gif', 'ico', 'txt', 'html', 'json']:
            return True
    return False 
        

run = True
now = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
HOST = ('127.0.0.1',7777)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(HOST)
sock.listen()

OK = b'HTTP/1.1 200 OK\n'
HEADERS = b"Host: some.ru\nHost1: some1.ru\nContent-Type: text/html; charset=utf-8\n\n"
ERR_404 = b'HTTP/1.1 404 Not Found\n\n'

while run:
    print ('-----------listen-----------')
    conn, addr = sock.accept()
    data = conn.recv(4096).decode()
    print(data)

    try:
        method, path, ver = data.split('\n')[0].split(" ",2)
        print("-----", method, path, ver)

        if is_file(path):
            send_file(path, conn)
        
        else:
            
            if path == '/':
                send_file('main.html', conn)
            
            elif path.startswith('/test'):
                test_list = path.split("/")
                html = f"<h1> тест с номером {test_list[1]} запущен <h1>"
                conn.send(OK)
                conn.send(HEADERS)
                conn.send(html.encode())
            
            elif path.startswith('/message'):
                message_list = path.split("/")
                html = f"<h1> {now} - сообщение от пользователя {message_list[1]} - {message_list[2]} <h1>"
                conn.send(OK)
                conn.send(HEADERS)
                conn.send(html.encode())

            else:
                html = f"<h1> пришли неизвестные  данные по HTTP - {path} <h1>"


                

    except Exception as e:
        conn.send(b'-------no http-------')
        print(e)