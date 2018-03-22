#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 15:03
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：前台表单

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Regexp, ValidationError, EqualTo
from app.models import User


# 会员登录表单
class LoginForm(FlaskForm):
    '''会员登录表单'''
    name = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "账号",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "密码",
        }
    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-lg btn-success btn-block"
        }
    )

    def validate_user(self, field):
        name = field.data
        admin = User.query.filter_by(name=name).count()
        if admin == 0:
            raise ValidationError('账号不存在！')


# 会员注册表单
class RegistForm(FlaskForm):
    '''会员注册表单'''
    name = StringField(
        label="昵称",
        validators=[
            DataRequired("请输入昵称!")
        ],
        description="昵称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入昵称",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱!"),
            Email("邮箱格式不正确!")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱",
        }
    )
    phone = StringField(
        label="手机",
        validators=[
            DataRequired("请输入手机号码!"),
            Regexp("^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}", message="手机号码格式不正确!")
        ],
        description="手机号码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机号码",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码!")
        ],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入密码",
        }
    )
    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请输入确认密码!"),
            EqualTo("pwd", "两次输入密码不一致！")
        ],
        description="确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入确认密码",
        }
    )
    submit = SubmitField(
        "注册",
        render_kw={
            "class": "btn btn-lg btn-success btn-block"
        }
    )

    def validate_name(self, field):
        name = field.data
        user_count = User.query.filter_by(name=name).count()
        if user_count == 1:
            raise ValidationError('用户昵称已经存在!')

    def validate_phone(self, field):
        phone = field.data
        user_count = User.query.filter_by(phone=phone).count()
        if user_count == 1:
            raise ValidationError('手机号码已经存在!')

    def validate_email(self, field):
        email = field.data
        user_count = User.query.filter_by(email=email).count()
        if user_count == 1:
            raise ValidationError('邮箱已经存在!')
