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
            template_folder = os.path.join(BASE_DIR, 'tamplates'),
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
    return render_template('user.html', users = users)


@app.route('/user_add/', methods = ['POST'])
def user_add():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        if user_name:
            db.session.add(User(user_name))
            db.session.commit()
    
    return redirect(url_for('index'))


@app.route('/quiz/', methods = ['GET', 'POST'])
def veiw_quiz():
    if request.method == 'GET':
        session['quiz_id'] = -1
        quizes = Quiz.query.all()
        return render_template('quizes.html', quizes = quizes)

    quiz_val = request.form.get('quiz')
    try:
        session['quiz_id'] = int(quiz_val)
    except (TypeError, ValueError):
        session['quiz_id'] = -1
    session['question_n'] = 0
    session['question_id'] = 0
    session['right_answer'] = 0
    return redirect(url_for('veiw_qustion'))


@app.route('/qustion/', methods = ['GET', 'POST'])
def veiw_qustion():
    quiz_id = session.get('quiz_id', -1)
    try:
        quiz_id = int(quiz_id)
    except (TypeError, ValueError):
        quiz_id = -1

    if quiz_id == -1:
        return redirect(url_for('view_quiz'))

    if request.method == 'POST':
        question = db.session.get(Question, session.get('question_id'))
        if question and question.answer == request.form.get('answer_text'):
            session['right_answer'] = session.get('right_answer', 0) + 1

        session['question_n'] = session.get('question_n', 0) + 1

    quiz = db.session.get(Quiz, quiz_id)
    if not quiz:
        session['quiz_id'] = -1
        return redirect(url_for('view_quiz'))

    if int(session.get('question_n', 0)) >= len(quiz.question):
        session['quiz_id'] = -1
        return redirect(url_for('view_result'))

    else:
        question = quiz.question[session.get('question_n', 0)]
        session['question_id'] = question.id
        answers = [question.answer, question.wrong1, question.wrong2, question.wrong3]
        shuffle(answers)

        return render_template('question.html',
                               answers = answers,
                               qustion = question
                               )
    

@app.route('/result/')
def view_result():
    return render_template('result.html',
                           right = session['right_answer'],
                           total = session['question_n']
                           )


@app.route('/quizes_view/', methods = ['GET', 'POST'])
def view_quiz_edit():
    quizes = Quiz.query.all()
    questions = Question.query.all()
    users = User.query.all()
    return render_template('quizes_view.html',
                           quizes=quizes,
                           questions=questions,
                           users = users
                           )

@app.route('/quiz_add/', methods = ['POST'])
def quiz_add():
    quiz_name = request.form.get('quiz_name')
    user_id = request.form.get('user_id')
    question_ids = request.form.getlist('question_ids')

    if quiz_name and user_id:
        user = db.session.get(User ,int(user_id))
        new_quiz = Quiz(quiz_name, user)

        for quiz_id in question_ids:
            question = db.session.get(Question, int(quiz_id))
            if question:
                new_quiz.question.append(question)

        db.session.add(new_quiz)
        db.session.commit()          
    
    return redirect(url_for('view_quiz_edit'))


@app.route('/question_add/', methods = ['POST'])
def question_add():
    question_text = request.form.get('question_text')
    correct_idx = int(request.form.get('correct_answer'))

    answers = [
        request.form.get('answear1'),
        request.form.get('answear2'),
        request.form.get('answear3'),
        request.form.get('answear4')
    ]  

    if question_text and all(answers):
        correct_answ = answers[correct_idx-1]
        wrong_answ = [ans for i, ans in enumerate(answers) if i != correct_idx -1]

        new_quest = Question(
            question=question_text,
            answer=correct_answ,
            wrong1=wrong_answ[0],
            wrong2=wrong_answ[1],
            wrong3=wrong_answ[2]
        )

        db.session.add(new_quest)
        db.session.commit()  
                
    
    return redirect(url_for('view_quiz_edit'))




@app.errorhandler(404)
def page_404(error):
    return render_template('404.html')

app.run(debug=True)