#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/6 11:28
# @Author  : hjy
# @File    : Main.py 入口函数

from app import app

if __name__ == '__main__':
    app.debug = True
    app.run()
