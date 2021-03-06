#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 15:03
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：管理员表单

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Admin, Tag, Auth, Role

# 查询所有标签
tags = Tag.query.all()
auth_lists = Auth.query.all()
role_lists = Role.query.all()

# 管理员登录表单
class LoginForm(FlaskForm):
    '''管理员登录表单'''
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号",
            # "required": "required"
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
            "placeholder": "请输入密码",
            # "required": "required"
        }
    )
    submit = SubmitField(
        "登录",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError('账号不存在！')


# 添加标签表单
class TagForm(FlaskForm):
    '''添加标签表单'''
    name = StringField(
        label="标签名称",
        validators=[
            DataRequired("请输入标签！")
        ],
        description="标签",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入标签名称",
            "id": "input_name"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 添加电影表单
class MovieForm(FlaskForm):
    '''添加电影表单'''
    title = StringField(
        label="片名",
        validators=[
            DataRequired("请输入片名！")
        ],
        description="片名",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片名",
            "id": "input_title"
        }
    )
    url = FileField(
        label="文件",
        validators=[
            DataRequired("请上传文件！")
        ],
        description="文件"
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
    logo = FileField(
        label="封面",
        validators=[
            DataRequired("请上传封面！")
        ],
        description="封面"
    )
    star = SelectField(
        label="星级",
        validators=[
            DataRequired("请选择星级！")
        ],
        coerce=int,
        choices=[(1, "1星"), (2, "2星"), (3, "3星"), (4, "4星"), (5, "5星")],
        description="星级",
        render_kw={
            "class": "form-control",
            "id": "input_star"
        }
    )
    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in tags],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_tag_id"
        }
    )
    area = StringField(
        label="地区",
        validators=[
            DataRequired("请输入地区！")
        ],
        description="地区",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区",
            "id": "input_area"
        }
    )
    length = StringField(
        label="片长",
        validators=[
            DataRequired("请输入片长！")
        ],
        description="片长",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片长",
            "id": "input_length"
        }
    )
    release_time = StringField(
        label="上映时间",
        validators=[
            DataRequired("请输入上映时间！")
        ],
        description="上映时间",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入上映时间",
            "id": "input_release_time"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 添加电影预告表单
class PreviewForm(FlaskForm):
    '''添加电影预告表单'''
    title = StringField(
        label="预告标题",
        validators=[
            DataRequired("请输入预告标题！")
        ],
        description="预告标题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入预告标题",
            "id": "input_title"
        }
    )
    logo = FileField(
        label="预告封面",
        validators=[
            DataRequired("请上传预告封面！")
        ],
        description="预告封面"
    )
    submit = SubmitField(
        "编辑",
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
        "修改",
        render_kw={
            "class": "btn btn-primary"
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["admin"]
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("旧密码错误！")


# 添加权限表单
class AuthForm(FlaskForm):
    '''添加权限表单'''
    name = StringField(
        label="权限名称",
        validators=[
            DataRequired("请输入权限名称！")
        ],
        description="权限名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限名称",
            "id": "input_name"
        }
    )
    url = StringField(
        label="权限地址",
        validators=[
            DataRequired("请输入权限地址！")
        ],
        description="权限地址",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入权限地址",
            "id": "input_url"
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 添加角色表单
class RoleForm(FlaskForm):
    '''添加角色表单'''
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired("请输入角色名称！")
        ],
        description="角色名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入角色名称",
            "id": "input_name"
        }
    )
    auths = SelectMultipleField(
        label="权限列表",
        validators=[
            DataRequired("请选择权限列表！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in auth_lists],
        description="权限列表",
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        "编辑",
        render_kw={
            "class": "btn btn-primary"
        }
    )


# 添加管理员表单
class AdminForm(FlaskForm):
    '''添加管理员表单'''
    name = StringField(
        label="管理员名称",
        validators=[
            DataRequired("请输入管理员名称！")
        ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员名称",
            "id": "input_name"
        }
    )
    pwd = PasswordField(
        label="管理员密码",
        validators=[
            DataRequired("请输入管理员密码！")
        ],
        description="管理员密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员密码",
            "id": "input_pwd"
        }
    )
    repwd = PasswordField(
        label="管理员重复密码",
        validators=[
            DataRequired("请输入管理员重复密码！"),
            EqualTo("pwd", "两次输入密码不一致！")
        ],
        description="管理员重复密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入管理员重复密码",
            "id": "input_re_pwd"
        }
    )
    role_id = SelectField(
        label="所属角色",
        validators=[
            DataRequired("请选择角色！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in role_lists],
        description="角色",
        render_kw={
            "class": "form-control",
            "id": "input_role_id"
        }
    )
    submit = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )
