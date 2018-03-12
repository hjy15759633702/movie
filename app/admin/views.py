#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 15:02
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：管理员视图

from . import admins
from flask import render_template, redirect, url_for


@admins.route("/")
def index():
    return render_template('admin/index.html')


# 管理员登录
@admins.route("/login/")
def login():
    return render_template('admin/login.html')


# 管理员退出
@admins.route("/logout/")
def logout():
    return redirect(url_for('admin.login'))


# 修改密码
@admins.route("/pwd/")
def pwd():
    return render_template('admin/pwd.html')


# 编辑标签
@admins.route("/tag/add/")
def tag_add():
    return render_template('admin/tag_add.html')


# 标签列表
@admins.route("/tag/list/")
def tag_list():
    return render_template('admin/tag_list.html')


# 编辑电影
@admins.route("/movie/add/")
def movie_add():
    return render_template('admin/movie_add.html')


# 电影列表
@admins.route("/tag/list/")
def movie_list():
    return render_template('admin/movie_list.html')


# 编辑上映预告
@admins.route("/preview/add/")
def preview_add():
    return render_template('admin/preview_add.html')


# 上映预告列表
@admins.route("/preview/list/")
def preview_list():
    return render_template('admin/preview_list.html')


# 会员列表
@admins.route("/user/list/")
def user_list():
    return render_template('admin/user_list.html')


# 查看会员
@admins.route("/user/view/")
def user_view():
    return render_template('admin/user_view.html')


# 评论列表
@admins.route("/comment/list/")
def comment_list():
    return render_template('admin/comment_list.html')


# 收藏列表
@admins.route("/moviecol/list/")
def moviecol_list():
    return render_template('admin/moviecol_list.html')


# 管理员登录日志列表
@admins.route("/adminloginlog/list/")
def adminloginlog_list():
    return render_template('admin/adminloginlog_list.html')


# 会员登录日志列表
@admins.route("/userloginlog/list/")
def userloginlog_list():
    return render_template('admin/userloginlog_list.html')


# 操作日志列表
@admins.route("/oplog/list/")
def oplog_list():
    return render_template('admin/oplog_list.html')


# 添加角色
@admins.route("/role/add/")
def role_add():
    return render_template('admin/role_add.html')


# 角色列表
@admins.route("/role/list/")
def role_list():
    return render_template('admin/role_list.html')


# 添加权限
@admins.route("/auth/add/")
def auth_add():
    return render_template('admin/auth_add.html')


# 权限列表
@admins.route("/auth/list/")
def auth_list():
    return render_template('admin/auth_list.html')


# 添加管理员
@admins.route("/admin/add/")
def admin_add():
    return render_template('admin/admin_add.html')


# 管理员列表
@admins.route("/admin/list/")
def admin_list():
    return render_template('admin/admin_list.html')
