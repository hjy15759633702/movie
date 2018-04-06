#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 15:03
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：前台表单

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField, TextAreaField
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
            "class": "form-control",
            "placeholder": "账号",
            "id": "name"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "密码",
            "id": "inputPassword3"
        }
    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-primary btn-block"
        }
    )


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
            "class": "btn btn-primary btn-block"
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


# 会员中心表单
class UserdetialForm(FlaskForm):
    '''会员中心表单'''
    name = StringField(
        label="昵称",
        validators=[
            DataRequired("请输入昵称!")
        ],
        description="昵称",
        render_kw={
            "class": "form-control",
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
            "class": "form-control",
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
            "class": "form-control",
            "placeholder": "请输入手机号码",
        }
    )
    face = FileField(
        label="头像",
        validators=[
            DataRequired("请上传头像！")
        ],
        description="头像"
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介！")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": "10",
            "id": "input_info"
        }
    )
    submit = SubmitField(
        '保存修改',
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 修改密码表单
class PwdForm(FlaskForm):
    '''修改密码表单'''
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码！")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码！")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入新密码",
        }
    )
    submit = SubmitField(
        "修改密码",
        render_kw={
            "class": "btn btn-primary"
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        user = User.query.filter_by(
            name=session["user"]
        ).first()
        if not user.check_pwd(pwd):
            raise ValidationError("旧密码错误！")


# 评论表单
class CommentForm(FlaskForm):
    '''评论表单'''
    comment = TextAreaField(
        label="内容",
        validators=[
            DataRequired("请输入内容！")
        ],
        description="内容",
        render_kw={
            "id": "input_content"
        }
    )
    submit = SubmitField(
        "提交评论",
        render_kw={
            "class": "btn btn-primary",
            "id": "btn-sub"
        }
    )
