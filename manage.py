#-*- coding:utf-8 -*-
from flask_script import Manager
from change_mysql import app
from flask_migrate import MigrateCommand,Migrate
from ext import db
from model import User,Question,Answer

manager = Manager(app)
migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()