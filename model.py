#-*- coding:utf-8 -*-
from ext import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    questions = db.relationship('Question',backref='author')

    def __init__(self,*args,**kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')

        self.telephone = telephone
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    question_id = db.Column(db.Integer,db.ForeignKey('questions.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    question = db.relationship('Question',backref=db.backref('answers'))
    author = db.relationship('User',backref=db.backref('answers'))
