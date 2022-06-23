import datetime
import os
from flask import Blueprint, render_template, jsonify, request, session, url_for, flash, send_file
from flask.views import MethodView
from flask_login import login_required, login_user, logout_user
from werkzeug.utils import redirect

from config import out_dir
from serve.DataBase import User, record_apply_mac, record_apply_info, get_my_apply, record_user
from serve.ExecLicMaker import exec_lic_maker_singel, zip_file, clean_temp_dir, exec_lic_maker_range
from serve.MacTool import is_mac, gen_mac_list, mac_17_2_12
from serve.form import LoginFrom, RegFrom
from serve import loginManager, db, ldap, app

index = Blueprint('index', __name__)


@loginManager.user_loader
def load_user(user_id):
    new = datetime.datetime.now()
    username = str(User.query.get(int(user_id)))
    user = User.query.filter_by(username=username).first()
    if user:
        old = user.last_login_time
        # 登录超时 3600s -> 1h
        if (new - old).seconds > 3600:
            user.is_login = False
            db.session.add(user)
            db.session.commit()
            session.clear()
            logout_user()
            app.logger.info('%s online time out, auto logout,last login time is:%s' % (username,old))
            return None
        return User.query.get(int(user_id))
    return User.query.get(int(user_id))




class RootView(MethodView):
    @login_required
    def get(self):
        app.logger.debug('from root view to index view')
        return redirect(url_for('index.index'))


class LoginView(MethodView):
    def get(self):
        if session.get('username') is not None:
            app.logger.debug('from login view to index view')
            return redirect(url_for('index.index'))
        form = LoginFrom()
        return render_template('login.html', form=form)

    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        app.logger.debug('user:%s try to login!'% username)
        # 前端已加防范，后端再防一手
        if username is None:
            app.logger.error('login with out username!')
            return jsonify({
                'code': 1,
                'message': '请输入用户名',
                'data': '', })
        if password is None:
            app.logger.error('login with out password!')
            return jsonify({
                'code': 1,
                'message': '请输入密码',
                'data': '', })
        # -------------login admin--------------------
        from config import admin_user,admin_password
        if (username == admin_user) & (password == admin_password):
            user = User.query.filter_by(username=username).first()
            user.is_login = True
            user.last_login_ip = request.remote_addr
            user.last_login_time = datetime.datetime.now()
            db.session.add_all([user])
            db.session.commit()
            login_user(user)
            session['username'] = username
            app.logger.info('admin is login !')
            return jsonify({
                'code': 0,
                'message': '登录成功！',
                'data': '',
            })
        # -------------------------------------------
        app.logger.debug('user:%s try to login!' % username)
        test = ldap.bind_user(username, password)
        # 查询到用户
        if test is not None:
            app.logger.info('user:%s is login! from addr:%s' % (username,request.remote_addr))
            user = User.query.filter_by(username=username).first()
            if user:
                user.is_login = True
                user.last_login_ip = request.remote_addr
                user.last_login_time = datetime.datetime.now()
                db.session.add_all([user])
                db.session.commit()
            else:
                app.logger.debug('new user:%s wire into DB!' % username)
                record_user(username, password, request.remote_addr)
                user = User.query.filter_by(username=username).first()
                # 记录登录信息
            login_user(user)
            app.logger.info('user:%s is login success!' % username)
            session['username'] = username
            return jsonify({
                'code': 0,
                'message': '登录成功！',
                'data': '',
            })
        app.logger.info('user:%s is login failed!' % username)
        return jsonify({
            'code': 1,
            'message': '用户名或密码错误',
            'data': '',
        })


class IndexView(MethodView):
    @login_required
    def get(self):
        app.logger.debug('user in index page')
        return render_template('index.html', my_apply=get_my_apply(session['username']))


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
        app.logger.info('user:%s is logout!'% username)
        return redirect(url_for('index.login', next=request.url))


class RegisterView(MethodView):
    def get(self):
        form = RegFrom()
        return render_template('register.html', form=form)

    def post(self):
        form = RegFrom()
        usernmae = request.form['username']
        pasword = request.form['password']
        setpasswod = request.form['se_password']
        key = request.form['key']
        if key != "admin":
            flash('请填写正确的邀请码，或向开发人员索取邀请码')
            return render_template('register.html', form=form)
        if pasword != setpasswod:
            flash('两次输入的密码不相同')
            return render_template('register.html', form=form)
        user = User.query.filter_by(username=usernmae).first()
        if user:
            flash('用户【%s】已存在' % usernmae)
            return render_template('register.html', form=form)
        new_user = User(username=usernmae)
        new_user.set_password(pasword)
        db.session.add(new_user)
        db.session.commit()
        flash('注册成功')
        return redirect(url_for('index.login'))


class ExecSingleView(MethodView):
    @login_required
    def get(self):
        try:
            clean_temp_dir()
            app.logger.debug('clean temp dir success!')
        except Exception as err:
            app.logger.error('clean temp dir failed :%s'%err)
        return render_template('single.html', my_apply=get_my_apply(session['username']))

    @login_required
    def post(self):
        # print(request.remote_addr)
        # 接收数据处理：由byte转str去除b''，去除空格，去除文本域name，以换行符分割mac存为列表
        data = request.form['mac_list'].replace(' ', '').replace('\r', '').split('\n')
        data_list = [x for x in data if x != '']
        app.logger.error('try ro exec single with mac:%s' % data_list)
        if (data_list == []) | (data_list is None):
            flash('请输入至少一个mac地址')
            app.logger.error('exec single without any mac!')
            return render_template('single.html', my_apply=get_my_apply(session['username']))
        else:
            apply_time = datetime.datetime.now()
            for mac in data_list:
                # 生成并改名
                if exec_lic_maker_singel(mac):
                    app.logger.info('make licence file with mac:%s success!' % mac)
                else:
                    app.logger.error('mac:%s 生成licence失败' % mac)
                    flash('mac:%s 生成licence失败' % mac)
                    app.logger.info('clean temp dir')
                    clean_temp_dir()
                    return render_template('single.html', my_apply=get_my_apply(session['username']))
            file_name = str(datetime.datetime.now()).split('.')[0].replace('-', '').replace(' ', '_').replace(':', '')[
                        2:-2] + '_' + session['username'].split('.')[0]
            if zip_file(file_name):
                clean_temp_dir()
                record_apply_info(apply_time, data_list, session['username'], request.remote_addr)
                record_apply_mac(data_list, apply_time)
                app.logger.info('exec single with all mac success!!')
                app.logger.info('send licence file :%s'% file_name)
                return send_file(os.path.join(out_dir, '%s.zip'% file_name))
            else:
                clean_temp_dir()
                app.logger.error('压缩:%s 失败!!!'%file_name)
                flash('压缩失败')
                return render_template('single.html', my_apply=get_my_apply(session['username']))


class ExecRangeView(MethodView):
    @login_required
    def get(self):
        return render_template('range.html', my_apply=get_my_apply(session['username']))

    @login_required
    def post(self):
        start_mac = request.form['start_mac']
        stop_mac = request.form['stop_mac']
        print(start_mac)
        print(stop_mac)
        app.logger.info('try to exec range with mac:%s to %s'%(start_mac,stop_mac))
        if (start_mac == '') | (stop_mac == ''):
            app.logger.error('exec range without start or stop mac!')
            flash('请输入开始和截止的mac地址')
            return render_template('range.html', my_apply=get_my_apply(session['username']))
        if is_mac(start_mac) & is_mac(stop_mac) is False:
            app.logger.error('exec single without True mac!')
            flash('请输入正确的开始和截止的mac地址')
            return render_template('range.html', my_apply=get_my_apply(session['username']))
        # 生成并改名
        apply_time = datetime.datetime.now()
        if int(mac_17_2_12(stop_mac), 16) < int(mac_17_2_12(start_mac), 16):
            start_mac, stop_mac = stop_mac, start_mac
        if exec_lic_maker_range(start_mac, stop_mac):
            app.logger.info('exec range with mac:%s to %s success!!'%(start_mac,stop_mac))
        else:
            app.logger.info('exec range with mac:%s to %s failed!!' % (start_mac, stop_mac))
            clean_temp_dir()
            flash('生成失败')
            return render_template('range.html', my_apply=get_my_apply(session['username']))
        file_name = str(datetime.datetime.now()).split('.')[0].replace('-', '').replace(' ', '_').replace(':', '')[
                    2:-2] + '_' + session['username'].split('.')[0]
        if zip_file(file_name):
            app.logger.debug('zip file success!')
            clean_temp_dir()
            mac_list = gen_mac_list(start_mac, stop_mac)
            record_apply_info(apply_time, mac_list, session['username'], request.remote_addr)
            record_apply_mac(mac_list, apply_time)
            app.logger.info('exec range with all mac success!!')
            app.logger.info('send licence file :%s' % file_name)
            return send_file(os.path.join(out_dir, '%s.zip'% file_name))
        else:
            clean_temp_dir()
            app.logger.error('压缩:%s 失败!!!' % file_name)
            flash('压缩失败')
            return render_template('range.html', my_apply=get_my_apply(session['username']))
