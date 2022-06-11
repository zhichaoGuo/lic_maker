import datetime
import json
import os
import time
import urllib
from urllib.parse import unquote

from flask import Blueprint, render_template, jsonify, request, session, url_for, flash, send_file
from flask.views import MethodView
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from config import out_dir
from serve.DataBase import User, Record, record_apply_mac, record_apply_info, get_my_apply
from serve.ExecLicMaker import exec_lic_maker_singel, zip_file, clean_temp_dir
from serve.form import LoginFrom
from serve import loginManager, db

index = Blueprint('index', __name__)


@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RootView(MethodView):
    @login_required
    def get(self):
        return redirect(url_for('index.index'))


class LoginView(MethodView):
    def get(self):
        form = LoginFrom()
        return render_template('login.html', form=form)

    def post(self):
        data = request.get_json()
        ip = request.remote_addr
        username = data['username']
        password = data['password']
        user = User.query.filter_by(username=username).first()
        db.session.add_all([user])
        db.session.commit()
        # 记录登录信息
        login_user(user)
        session['username'] = username
        return jsonify({
            'code': 0,
            'message': 'message',
            'data': '',
        })


class IndexView(MethodView):
    @login_required
    def get(self):
        return render_template('index.html',my_apply=get_my_apply(session['username']))

class LogoutView(MethodView):
    @login_required
    def get(self):
        username = session.get("username")
        session.clear()
        logout_user()
        user = User.query.filter_by(username=username).first()
        user.is_login = False
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index.login', next=request.url))


class ExecSingleView(MethodView):
    @login_required
    def get(self):
        clean_temp_dir()
        return render_template('single.html')
    @login_required
    def post(self):
        print(request.remote_addr)
        # 接收数据处理：由byte转str去除b''，去除空格，去除文本域name，以换行符分割mac存为列表
        data = request.get_json()['mac_str'].replace(' ','').split('\n')
        data_list = [x for x in data if x != '']
        # data_list = urllib.parse.unquote(str(data_byte)[2:-1].replace("+", "")).split("=")[1].split("\r\n")
        # 去除列表空值（多余换行）
        # data_list = [i for i in data_list if i != '']
        if (data_list == []) | (data_list is None):
            flash('请输入至少一个mac地址')
            return render_template('single.html',my_apply=get_my_apply(session['username']))
        else:
            apply_time = datetime.datetime.now()
            for mac in data_list:
                # 生成并改名
                if exec_lic_maker_singel(mac):
                    # 执行成功，记录操作和mac
                    record_apply_info(apply_time,mac,session['username'],request.remote_addr)
                    record_apply_mac(mac,apply_time)
                else:
                    flash('mac:%s 生成licence失败'%mac)
                    return render_template('single.html',my_apply=get_my_apply(session['username']))
            if zip_file('test'):
                clean_temp_dir()
                return send_file(os.path.join(out_dir,'test.zip'))
            else:
                flash('压缩失败')
                return render_template('single.html',my_apply=get_my_apply(session['username']))
        # return jsonify({
        #     'code': 0,
        #     'message': '生成成功',
        #     'data': '',
        # }
        # )

class ExecRangeView(MethodView):
    @login_required
    def get(self):
        return render_template('range.html',my_apply=get_my_apply(session['username']))
    @login_required
    def post(self):
        data = request.get_json() # data={"start_mac":"00:1f:c1:00:00:00","stop_mac":"00:1f:c1:00:00:01","method":"range"}
        # 生成licence
        return jsonify({
            'code': 0,
            'message': '生成成功',
            'data': '',
        }
    )