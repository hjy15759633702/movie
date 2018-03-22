#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 15:02
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：前台视图

from . import homes
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import RegistForm, LoginForm
from app.models import User, Userlog
from app import db
import uuid
from werkzeug.security import generate_password_hash


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
        return redirect(request.args.get('next') or url_for("home.index"))
    return render_template('home/login.html', form=form)


# 退出
@homes.route("/logout/")
def logout():
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
@homes.route("/user/")
def user():
    return render_template('home/user.html')


# 修改密码
@homes.route("/pwd/")
def pwd():
    return render_template('home/pwd.html')


# 评论
@homes.route("/comments/")
def comments():
    return render_template('home/comments.html')


# 登录日志
@homes.route("/loginlog/")
def loginlog():
    return render_template('home/loginlog.html')


# 电影收藏
@homes.route("/moviecol/")
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
