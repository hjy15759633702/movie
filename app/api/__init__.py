#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/27 15:43
# @Author  : hjy
# @File    : __init__.py.py

from flask import Blueprint

apis = Blueprint('api', __name__)

import app.api.views