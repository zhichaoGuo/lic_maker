import datetime

from werkzeug.security import generate_password_hash

from serve import db


class User(db.Model):  # 用户表
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(63), unique=True)
    password = db.Column(db.String(252))
    last_login_ip = db.Column(db.String(15))
    last_login_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    status = db.Column(db.Boolean(), default=False)
    is_login = db.Column(db.Boolean(), default=False)
    is_free = db.Column(db.Boolean(), default=False)
    freetime = db.Column(db.DateTime(), default=datetime.datetime.now())

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return True
        # return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Record(db.Model):  # 申请记录表
    __tablename__ = 'record'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    apply_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    apply_mac = db.Column(db.String(252))
    apply_user = db.Column(db.String(252))
    apply_ip = db.Column(db.String(252))


class MacList(db.Model):  # mac申请记录表
    __tablename__ = 'mac_list'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    mac = db.Column(db.String(252))
    first_apply_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    last_apply_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    apply_num = db.Column(db.Integer())


def record_apply_mac(mac, apply_time):
    mac_item = MacList.query.filter_by(mac=mac).first()
    if mac_item:
        mac_item.last_apply_time = apply_time
        mac_item.apply_num += 1
        db.session.commit()
    else:
        new_mac = MacList(mac=mac, first_apply_time=apply_time, last_apply_time=apply_time, apply_num=1)
        db.session.add(new_mac)
        db.session.commit()


def record_apply_info(time, mac, user, ip):
    if type(mac) is str:
        new_record = Record(apply_time=time, apply_mac=mac, apply_user=user, apply_ip=ip)
        db.session.add(new_record)
        db.session.commit()
    elif type(mac) is list:
        for mac_one in mac:
            new_record = Record(apply_time=time, apply_mac=mac, apply_user=user, apply_ip=ip)
            db.session.add(new_record)
        db.session.commit()
    return True


def get_my_apply(user):
    return Record.query.filter_by(apply_user=user)
