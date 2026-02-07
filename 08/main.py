from flask import Flask, redirect, render_template, request, session, url_for, jsonify
import os
from models import db, db_add_new_data, User, Quiz, Question
from random import shuffle

BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, 'db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

DB_PATH = os.path.join(DB_DIR, 'db_quiz.db')


app = Flask(__name__,
            template_folder = os.path.join(BASE_DIR, 'tamplate'),
            static_folder = os.path.join(BASE_DIR, 'static')
            )

app.config['SECRET_KEY'] = 'veryvery_secret_key_in_world'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'

db.init_app(app)

with app.app_context():
    db_add_new_data()


@app.route('/', methods = ['GET'])
def index():
    users = User.query.order_by(User.name).all()
    return render_template('base.html')

app.run(debug=True)