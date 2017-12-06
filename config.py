#-*- coding:utf-8 -*-

import os

DEBUG = True
SECRET_KEY = os.urandom(24)
#mysql数据库格式：dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = '1111'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'db_demo'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
