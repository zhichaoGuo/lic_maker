import logging
import subprocess
from logging.handlers import TimedRotatingFileHandler
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from serve.index import index
from flask import Flask
from config import *

app = Flask(__name__)

app.register_blueprint(index)
app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'

server_log = TimedRotatingFileHandler('server.log', 'D')
server_log.setLevel(logging.DEBUG)
server_log.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))

error_log = TimedRotatingFileHandler('error.log', 'D')
error_log.setLevel(logging.ERROR)
error_log.setFormatter(logging.Formatter('%(asctime)s: %(message)s [in %(pathname)s:%(lineno)d]'))

app.logger.addHandler(server_log)
app.logger.addHandler(error_log)
app.logger.info('123123123')
app.secret_key = 'Htek20180905'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
if os.path.exists(os.path.join(root_dir,'database')) is False:
    os.mkdir(os.path.join(root_dir,'database'))
from .DataBase import *
db.create_all()

loginManager = LoginManager(app)
loginManager.session_protection = "strong"
loginManager.login_view = 'index.login'
loginManager.login_message = u'lic_maker平台必须登录，请登录您的平台账号！'

subprocess.run(['sudo','chmod','777','lic_maker'], cwd=root_dir, timeout=10)
subprocess.run(['sudo','chmod','777','zpipe'], cwd=root_dir, timeout=10)
