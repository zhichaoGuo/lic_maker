import datetime

from sqlalchemy import desc, event
from werkzeug.security import generate_password_hash, check_password_hash

from serve import db, app


class User(db.Model):  # 用户表
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(63), unique=True)
    password = db.Column(db.String(252))
    last_login_ip = db.Column(db.String(15))
    last_login_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    status = db.Column(db.Boolean(), default=False)
    is_login = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.username

    def set_password(self, password):
        app.logger.info('%s set password' % self.username)
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # return True
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


@event.listens_for(User.__table__, 'after_create')
def create_admin(*args, **kwargs):
    from config import admin_user,admin_password
    app.logger.info('create admin account:%s'%admin_user)
    admin = User(username=admin_user)
    admin.set_password(admin_password)
    db.session.add(admin)
    db.session.commit()


class Record(db.Model):  # 申请记录表
    __tablename__ = 'record'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    apply_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    apply_mac = db.Column(db.String(252))
    apply_user = db.Column(db.String(252))
    apply_ip = db.Column(db.String(252))


class MacList(db.Model):  # mac记录表
    __tablename__ = 'mac_list'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    mac = db.Column(db.String(252), unique=True)
    first_apply_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    last_apply_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    apply_num = db.Column(db.Integer())


def record_user(username, password, login_ip):
    app.logger.info('record user:%s'% username)
    new_user = User(username=username, last_login_ip=login_ip, last_login_time=datetime.datetime.now(), is_login=True)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()


def record_apply_mac(mac, apply_time):
    if type(mac) == str:
        mac_item = MacList.query.filter_by(mac=mac).first()
        if mac_item:
            app.logger.info('record mac:%s' % mac)
            mac_item.last_apply_time = apply_time
            mac_item.apply_num += 1
            db.session.commit()
        else:
            app.logger.info('record new mac:%s' % mac)
            new_mac = MacList(mac=mac, first_apply_time=apply_time, last_apply_time=apply_time, apply_num=1)
            db.session.add(new_mac)
            db.session.commit()
    elif type(mac) == list:
        app.logger.info('record mac:%s' % mac)
        for mac_one in mac:
            mac_item = MacList.query.filter_by(mac=mac_one).first()
            if mac_item:
                mac_item.last_apply_time = apply_time
                mac_item.apply_num += 1
                db.session.commit()
            else:
                new_mac = MacList(mac=mac_one, first_apply_time=apply_time, last_apply_time=apply_time, apply_num=1)
                db.session.add(new_mac)
                db.session.commit()


def record_apply_info(time, mac, user, ip):
    if type(mac) is str:
        new_record = Record(apply_time=time, apply_mac=mac, apply_user=user, apply_ip=ip)
        db.session.add(new_record)
        db.session.commit()
    elif type(mac) is list:
        for mac_one in mac:
            new_record = Record(apply_time=time, apply_mac=mac_one, apply_user=user, apply_ip=ip)
            db.session.add(new_record)
        db.session.commit()
    return True


def get_my_apply(user):
    from config import admin_user
    if user == admin_user:
        return Record.query.all()
    else:
        return Record.query.filter_by(apply_user=user).order_by(desc(Record.apply_time))
