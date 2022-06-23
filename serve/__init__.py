import logging
import subprocess
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_simpleldap import LDAP
from flask import Flask
from config import *
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)
# -------------  setting logging  -----------------
logging.basicConfig(level=logging.DEBUG)
if not os.path.exists(log_dir):  # os模块判断并创建
    os.mkdir(log_dir)
formatter = logging.Formatter("[%(asctime)s][%(module)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
handler = TimedRotatingFileHandler("./log/flask.log", when="D", interval=1, backupCount=15, encoding="UTF-8", delay=False, utc=True)
app.logger.addHandler(handler)
handler.setFormatter(formatter)
app.logger.info('init server!')

app.secret_key = 'Htek20180905'
# -------------  setting database  -----------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
if os.path.exists(os.path.join(root_dir,'database')) is False:
    os.mkdir(os.path.join(root_dir,'database'))
from .DataBase import *
db.create_all()
# -------------  setting login   -----------------
loginManager = LoginManager(app)
loginManager.session_protection = "strong"
loginManager.login_view = 'index.login'
loginManager.login_message = u'lic_maker平台必须登录，请登录您的平台账号！'

# -------------  setting ldap  -----------------
app.config["LDAP_HOST"] = "192.168.0.164"
app.config["LDAP_PORT"] = 389
app.config["LDAP_USER_OBJECT_FILTER"] = "(&(objectclass=Person)(sAMAccountName=%s))"
app.config["LDAP_BASE_DN"] = "ou=htek,dc=htek,dc=org"
app.config["LDAP_USERNAME"] = "cn=ldapadmin,ou=htek,dc=htek,dc=org"
app.config["LDAP_PASSWORD"] = "LDap123"
ldap = LDAP(app)

# -------------  change mod for lic_maker  -----------------
subprocess.run(['sudo','chmod','777','lic_maker'], cwd=root_dir, timeout=10)
subprocess.run(['sudo','chmod','777','zpipe'], cwd=root_dir, timeout=10)
