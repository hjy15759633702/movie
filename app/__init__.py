#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 14:30
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：项目初始化

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'movie'
USERNAME = 'root'
PASSWORD = 'hjy'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:hjy@127.0.0.1:3306/movie?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = '173fe082661a4359b5f425392d9877c4'

# 电影资源
app.config["UP_DIR_MOVIE"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/movie/")
# 电影log图片
app.config["UP_DIR_MOVIE_IMG"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/movie/image/")
# 会员头像图片
app.config["UP_DIR_HEAD"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/head/")
# 跟目录
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")
# 电影预告图片
app.config["UP_DIR_PREVIEW"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/preview/")

app.debug = True

db = SQLAlchemy(app)

from app.home import homes as home_blueprint
from app.admin import admins as admin_blueprint
from app.api import apis as api_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(api_blueprint, url_prefix="/api")

# 404页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404
