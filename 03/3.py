'''

Написать веб-приложение на Flask со следующими ендпоинтами:
    - главная страница - содержит ссылки на все остальные страницы
    - /duck/ - отображает заголовок "рандомная утка №ххх" и картинка утки 
                которую получает по API https://random-d.uk/api/random
                
    - /fox/<int>/ - аналогично утке только с лисой (- https://randomfox.ca), 
                    но количество разных картинок определено int. 
                    если int больше 10 или меньше 1 - вывести сообщение 
                    что можно только от 1 до 10
    
    - /weather-minsk/ - показывает погоду в минске в красивом формате
    
    - /weather/<city>/ - показывает погоду в городе указанного в city
                    если такого города нет - написать об этом
    
    - по желанию добавить еще один ендпоинт на любую тему 
    
    
Добавить обработчик ошибки 404. (есть в example)
    

'''


from flask import (Flask, render_template,
                   session, request, redirect, url_for)

import requests
import os
import random
import re

BASE_DIR = os.path.dirname(__file__)

app = Flask(__name__,
            template_folder = os.path.join(BASE_DIR, 'templates'),
            static_folder = os.path.join(BASE_DIR, 'static'))

app.config['SECRET_KEY'] = 'my secret key'
user_db = {}

def random_fox():
    return random.randint(1, 10)

def login_check():
    return 'user' in session

def valid_regist(form):
    err = []

    name = form.get('name', '').strip()
    surname = form.get('surname', '').strip()
    login = form.get('login', '').strip()
    password = form.get('password', '').strip()

    if not re.fullmatch(r'[А-Яа-яЁё]+', name):
        err.append('The name must contain only Russian letters.')
    
    if not re.fullmatch(r'[А-Яа-яЁё]+', surname):
        err.append('The surname must contain only Russian letters.')
    
    if not re.fullmatch(r'[A-Za-z0-9_]{6,20}', login):
        err.append('The login must contain Latin letters, numbers and _.' \
                  ' The number of characters must be from 6 to 20 characters.')
    
    if login in user_db:
        err.append('The login is already taken')
    
    if not re.fullmatch(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,15}', password):
        err.append('The password must contain at least one lowercase Latin letter, one uppercase letter, and one number. ' \
                   'It must be between 8 and 15 characters long.')
    
    return err 

@app.route('/base/')
@app.route('/')
def index():
    return render_template('index.html', rnd = random_fox())


@app.route('/duck/')
def duck():
    if not login_check():
        return redirect(url_for('sign_up'))
    
    res = requests.get("https://random-d.uk/api/random")
    img_url = res.json()['url']
    num_img = img_url.split('/')[-1].split('.')[0]

    return render_template('duck.html', rnd = random_fox(), num = num_img, imag = img_url)

@app.route('/fox/<int:num>/')
def fox(num):
    if not login_check():
        return redirect(url_for('sign_up'))

    if num < 1 or num > 10:
        return f"Only from 1 to 10 is allowed"

    
    foxes = []
    for f in range(num):
        res = requests.get("https://randomfox.ca/floof/")
        data = res.json()
        foxes.append(data.get('image'))

    return render_template('fox.html', rnd = random_fox(), foxes = foxes, num = num)

@app.route('/weather-minsk/')
def weather_minsk():
    if not login_check():
        return redirect(url_for('sign_up'))

    url = f'http://api.openweathermap.org/data/2.5/weather'
    params = {'q':'Minsk', 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}
    res = requests.get(url, params)
    res = res.json()

    cl = res["weather"][0]["description"]
    temp = int(res["main"]["temp"])-273
    temp_feel =int(res["main"]["feels_like"])-273
    humid = res["main"]["humidity"]
    press = res["main"]["pressure"]

    return render_template('weather_minsk.html',
                           rnd = random_fox(),
                           cl = cl,
                           temp = temp,
                           temp_feel = temp_feel,
                           humid = humid,
                           press = press)

@app.route('/weather/<city>/')
def weather_city(city):
    if not login_check():
        return redirect(url_for('sign_up'))
    
    rnd = random_fox()
    url = f'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city , 'APPID': '2a4ff86f9aaa70041ec8e82db64abf56'}
    res = requests.get(url, params)
    res = res.json()

    if res.get('cod') != 200:
        return f"City '{city}' not found"

    cl = res["weather"][0]["description"]
    temp = int(res["main"]["temp"])-273
    temp_feel =int(res["main"]["feels_like"])-273
    humid = res["main"]["humidity"]
    press = res["main"]["pressure"]

    return render_template('weather_city.html',
                           rnd = random_fox(),
                           city = city,
                           cl = cl,
                           temp = temp,
                           temp_feel = temp_feel,
                           humid = humid,
                           press = press)



@app.route('/candle/')
def candle():
    if not login_check():
        return redirect(url_for('sign_up'), rnd = random_fox())
    
    return render_template('candle.html')

@app.route('/regist/', methods = ['GET', 'POST'])
def regist():
    if login_check():
        return redirect(url_for('index'))

    err = []
    form_data = {}

    if request.method == 'POST':
        form_data = request.form.to_dict()
        err = valid_regist(request.form)

        if not err:
            user_db[form_data['login']] ={
                'name': form_data['name'],
                'surname': form_data['surname'],
                'password': form_data['password']
            }
            return redirect(url_for('sign_up'))

    return render_template('register.html', err = err , form = form_data)

@app.route('/sign-up/', methods = ['GET', 'POST'])
def sign_up():
    if login_check():
        return redirect(url_for('index'))
    
    err = None

    if request.method == 'POST':
        login_val = request.form.get('login')
        password = request.form.get('password')

        user = user_db.get(login_val)

        if user and user['password'] == password:
            session['user'] = {
                'login': login_val,
                'name': user['name'],
                'surname': user['surname']
            }
            return redirect(url_for('index'))
        
        else:
            err = 'Incorrect login or password'
            

    return render_template('sign_up.html', err = err)


@app.route('/logout/')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/home_5/')
def home_5():
    return render_template('task_5.html', rnd = random_fox())


@app.errorhandler(404)
def page_not_found(err):
    return '<h1 style="color:red"> такой страницы не существует </h1>'




app.run(debug=True, host='0.0.0.0')
