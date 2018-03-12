#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 14:30
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：项目初始化

from flask import Flask, render_template

app = Flask(__name__)

from app.home import homes as home_blueprint
from app.admin import admins as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")


# 404页面
@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404
