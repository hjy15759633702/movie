#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/27 15:46
# @Author  : hjy
# @File    : view.py
# @Detial  ：api接口初始化

from app.api import apis
import json

# 登录
@apis.route("/login/", methods=['POST'])
def login():
    return json.dumps(dict(res=1))