#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 15:36
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：数据模块models


import pymysql
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'movie'
USERNAME = 'root'
PASSWORD = 'hjy'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:hjy@127.0.0.1:3306/movie?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = '173fe082661a4359b5f425392d9877c4'
db = SQLAlchemy(app)
# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名字
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 电话
    info = db.Column(db.Text)  # 简介
    status = db.Column(db.String(1), default=0)  # 状态 0 激活 1 冻结
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    uuid = db.Column(db.String(255))  # 唯一标识

    uselogs = db.relationship("Userlog", backref='user')  # 会员日志外键关联关系
    comments = db.relationship("Comment", backref='user')  # 评论外键关联关系
    moviecols = db.relationship("Moviecol", backref='user')  # 电影收藏关联关系

    def __repr__(self):
        return "<User %r>" % self.name


# 会员登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    ip = db.Column(db.String(100))  # 登录ip
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 用户外键

    def __repr__(self):
        return '<Userlog %r>' % self.id


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    movies = db.relationship('Movie', backref='tag')  # 电影外键关系关联

    def __repr__(self):
        return '<Tag %r>' % self.name


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # 地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论量
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签 标签外键

    comments = db.relationship("Comment", backref='movie')  # 评论外键关联关系
    moviecols = db.relationship("Moviecol", backref='movie')  # 电影收藏关联关系

    def __repr__(self):
        return '<Movie %r>' % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Preview %r>' % self.title


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)  # 评论内容
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 电影外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 用户外键

    def __repr__(self):
        return '<Comment %r>' % self.id


# 电影收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 电影外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 用户外键

    def __repr__(self):
        return '<Moviecol %r>' % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<Auth %r>' % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(500))  # 权限列表字符串
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    admins = db.relationship("Admin", backref='role')  # 管理员外键关联关系

    def __repr__(self):
        return '<Role %r>' % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名字
    pwd = db.Column(db.String(100))  # 密码
    is_super = db.Column(db.SmallInteger)  # 是否是超级管理员 0是超级管理员
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 角色外键  所属角色

    adminlogs = db.relationship("Adminlog", backref='admin')  # 管理员登录日志外键关联关系
    oplogs = db.relationship("Oplog", backref='admin')  # 操作日志外键关联关系

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    ip = db.Column(db.String(100))  # 登录ip
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 管理员外键

    def __repr__(self):
        return '<Adminlog %r>' % self.id


# 操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    ip = db.Column(db.String(100))  # 登录ip
    reason = db.Column(db.String(500))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间

    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 管理员外键

    def __repr__(self):
        return '<Oplog %r>' % self.id


if __name__ == '__main__':
    db.create_all()
    '''
    role = Role(
        name="超级管理员",
        auths=""
    )
    db.session.add(role)
    db.session.commit()
    
    from werkzeug.security import generate_password_hash
    admin = Admin(
        name="hjy",
        pwd=generate_password_hash('hjy'),
        is_super=0,
        role_id=1
    )
    db.session.add(admin)
    db.session.commit()
    '''
