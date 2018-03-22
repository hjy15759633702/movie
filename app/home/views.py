#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 15:02
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：前台视图

from . import homes
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import RegistForm, LoginForm, UserdetialForm
from app.models import User, Userlog
from app import db, app
import uuid
from werkzeug.security import generate_password_hash
from functools import wraps
import os
import datetime


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


# 验证是否处于登录
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 列表
@homes.route("/")
def index():
    return render_template('home/index.html')


# 登录
@homes.route("/login/", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        # 账号冻结
        if not user.status == 0:
            flash("该账号已经被冻结了，请联系客服！", 'err')
            return redirect(url_for("home.login"))

        if not user.check_pwd(data['pwd']):
            flash("密码错误！", 'err')
            return redirect(url_for("home.login"))
        session['user'] = data['name']
        session['user_id'] = user.id
        userlog = Userlog(
            user_id=session['user_id'],
            ip=request.remote_addr,
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(url_for("home.user"))
    return render_template('home/login.html', form=form)


# 退出
@homes.route("/logout/")
@user_login_req
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('home.login'))


# 注册
@homes.route("/regist/", methods=['POST', 'GET'])
def regist():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            pwd=generate_password_hash(data['pwd']),
            email=data['email'],
            phone=data['phone'],
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("会员注册成功！", 'ok')
        return redirect(url_for("home.regist"))
    return render_template('home/regist.html', form=form)


# 会员中心
@homes.route("/user/", methods=['POST', 'GET'])
@user_login_req
def user():
    form = UserdetialForm()
    user = User.query.get_or_404(int(session['user_id']))
    form.face.validators = []
    if request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data

        name_count = User.query.filter_by(name=data['name']).count()
        if name_count == 1 and user.name != data['name']:
            flash("用户昵称已经存在！", 'err')
            return redirect(url_for("home.user"))

        email_count = User.query.filter_by(email=data['email']).count()
        if email_count == 1 and user.email != data['email']:
            flash("邮箱已经存在！", 'err')
            return redirect(url_for("home.user"))

        phone_count = User.query.filter_by(phone=data['phone']).count()
        if phone_count == 1 and user.phone != data['phone']:
            flash("手机号码已经存在！", 'err')
            return redirect(url_for("home.user"))

        if not os.path.exists(app.config["UP_DIR_HEAD"]):
            os.makedirs(app.config["UP_DIR_HEAD"])
            os.chmod(app.config["UP_DIR_HEAD"], "rw")

        if form.face.data != "":
            file_face = str(form.face.data)
            # 删除原来资源
            # file_del(app.config["UP_DIR_MOVIE_IMG"], movie.logo)
            user.face = change_filename(file_face)
            form.face.data.save(app.config["UP_DIR_HEAD"] + user.face)

        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']
        db.session.add(user)
        db.session.commit()
        flash("会员信息修改成功！", 'ok')
        return redirect(url_for("home.user"))
    return render_template('home/user.html', form=form, user=user)


# 修改密码
@homes.route("/pwd/")
@user_login_req
def pwd():
    return render_template('home/pwd.html')


# 评论
@homes.route("/comments/")
def comments():
    return render_template('home/comments.html')


# 登录日志
@homes.route("/loginlog/")
@user_login_req
def loginlog():
    return render_template('home/loginlog.html')


# 电影收藏
@homes.route("/moviecol/")
@user_login_req
def moviecol():
    return render_template('home/moviecol.html')


# 动画
@homes.route("/animation/")
def animation():
    return render_template('home/animation.html')


# 搜索
@homes.route("/search/")
def search():
    return render_template('home/search.html')


# 电影播放
@homes.route("/play/")
def play():
    return render_template('home/play.html')
