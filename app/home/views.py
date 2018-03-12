#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 15:02
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：前台视图

from . import homes
from flask import render_template, redirect, url_for


# 列表
@homes.route("/")
def index():
    return render_template('home/index.html')


# 登录
@homes.route("/login/")
def login():
    return render_template('home/login.html')


# 退出
@homes.route("/logout/")
def logout():
    return redirect(url_for('home.login'))


# 注册
@homes.route("/regist/")
def regist():
    return render_template('home/regist.html')


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
