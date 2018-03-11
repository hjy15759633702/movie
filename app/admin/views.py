#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 15:02
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：管理员视图

from . import admin

@admin.route("/")
def admin():
    return "admin"

