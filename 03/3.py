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


from flask import Flask, render_template
import requests
import os
import random

BASE_DIR = os.path.dirname(__file__)

app = Flask(__name__,
            template_folder = os.path.join(BASE_DIR, 'templates'),
            static_folder = os.path.join(BASE_DIR, 'static'))

@app.route('/')
def index():
    rnd = random.randint(1, 10)
    return render_template('index.html', rnd = rnd)

@app.route('/duck/')
def duck():
    res = requests.get("https://random-d.uk/api/random")
    img_url = res.json()['url']
    num_img = img_url.split('/')[-1].split('.')[0]

    return render_template('duck.html', num = num_img, imag = img_url)

@app.route('/fox/<int:num>/')
def fox(num):
    if num < 1 or num > 10:
        return f"Only from 1 to 10 is allowed"

    foxes = []
    for f in range(num):
        res = requests.get("https://randomfox.ca/floof/")
        data = res.json()
        foxes.append(data.get('image'))

    return render_template('fox.html',  foxes = foxes)

@app.route('/weather-minsk/')
def weather_minsk():
    return render_template('weather_minsk.html')

@app.route('/weather/<city>/')
def weather_city(city):
    return render_template('weather_city.html', city = city)

@app.route('/candle/')
def candle():
    return render_template('candle.html')






app.run(debug=True)
