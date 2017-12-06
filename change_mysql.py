# -*- coding:utf-8 -*-

from flask import Flask,session,render_template,request,redirect,url_for,g
# from flask_login import login_required,LoginManager
from ext import db
import config
from model import User,Question,Answer
from datetime import timedelta
from sqlalchemy import or_      #查询关键字用。一般在标题或者内容里同时查询，即多个字段查询
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
# login_manager = LoginManager(app)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)


@app.route('/')
def index():
    context = {
        'questions':Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)


@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'手机号码或者密码错误，确认后登录'

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method=='GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已被注册，请更换手机号码或直接登录'
        else:
            if password1 != password2:
                return u'两次密码不相等，请核对后再填写'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                return redirect(url_for('login'))


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    if hasattr(g,'user'):
        return {'user':g.user}
    return { }


@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))


@app.route('/question/',methods=['GET','POST'])
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        body = Question(
                        title=request.form.get('title'),
                        content=request.form.get('content'),
                        author_id=session.get('user_id')
                        )
        db.session.add(body)
        return redirect(url_for('index'))


@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id==question_id).first()
    return render_template('detail.html',question=question_model)



@app.route('/add_answer/',methods=['POST'])
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    question = Question.query.filter(Question.id == question_id).first()
    answer = Answer(content=content)
    answer.author = g.user
    answer.question = question
    db.session.add(answer)
    return redirect(url_for('detail',question_id=question_id))


@app.route('/search/')
def search():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q))).order_by('-create_time')
    return render_template('index.html',questions=questions)

if __name__ == '__main__':
    app.run( )
