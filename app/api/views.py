#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/27 15:46
# @Author  : hjy
# @File    : views.py
# @Detial  ：api接口初始化

from flask import request, jsonify, current_app
from app.api import apis
from functools import wraps
from app.models import User
import redis

redis_store = redis.Redis(host='127.0.0.1', port=6070, db=4, password='hjy')

def login_check(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return jsonify({'code': 0, 'message': u'需要验证'})

        name = current_app.redis.get('token:%s' % token)

        if not name or token != current_app.redis.hget('user:%s' % name, 'token'):
            return jsonify({'code': 2, 'message': u'验证信息错误'})

        return f(*args, **kwargs)

    return decorator


# @apis.before_request
# def before_request():
#     token = request.headers.get('token')
#     name = current_app.redis.get('token:%s' % token)
#     if name:
#         g.current_user = User.query.filter_by(name=name).first()
#         g.token = token
#     return
#
#
# @apis.route('/login', methods=['POST'])
# def login():
#     phone_number = request.get_json().get('phone_number')
#     password = request.get_json().get('password')
#     user = User.query.filter_by(phone_number=phone_number).first()
#     if not user:
#         return jsonify({'code': 0, 'message': '没有此用户'})
#
#     if user.password != password:
#         return jsonify({'code': 0, 'message': '密码错误'})
#
#     m = hashlib.md5()
#     m.update(phone_number)
#     m.update(password)
#     m.update(str(int(time.time())))
#     token = m.hexdigest()
#
#     pipeline = current_app.redis.pipeline()
#     pipeline.hmset('user:%s' % user.phone_number, {'token': token, 'nickname': user.nickname, 'app_online': 1})
#     pipeline.set('token:%s' % token, user.phone_number)
#     pipeline.expire('token:%s' % token, 3600 * 24 * 30)
#     pipeline.execute()
#
#     return jsonify({'code': 1, 'message': '成功登录', 'nickname': user.nickname, 'token': token})
