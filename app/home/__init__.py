#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 14:30
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：前台初始化

from flask import Blueprint

homes = Blueprint('home', __name__)

import app.home.views