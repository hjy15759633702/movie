#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 14:56
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：管理员模块初始化

from flask import Blueprint

admins = Blueprint('admin', __name__)

import app.admin.views
