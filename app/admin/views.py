#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 15:02
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：管理员视图

from . import admins
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm, TagForm, MovieForm
from app.models import Admin, Tag, Movie
from functools import wraps
from app import db, app
from werkzeug.utils import secure_filename
import os
import uuid
import datetime


# 验证是否处于登录
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@admins.route("/")
@admin_login_req
def index():
    return render_template('admin/index.html')


# 管理员登录
@admins.route("/login/", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if not admin.check_pwd(data['pwd']):
            flash("密码错误！")
            return redirect(url_for("admin.login"))
        session['admin'] = data['account']
        return redirect(request.args.get('next') or url_for("admin.index"))
    return render_template('admin/login.html', form=form)


# 管理员退出
@admins.route("/logout/")
@admin_login_req
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


# 修改密码
@admins.route("/pwd/")
@admin_login_req
def pwd():
    return render_template('admin/pwd.html')


# 添加标签
@admins.route("/tag/add/", methods=['POST', 'GET'])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag_count == 1:
            flash("标签已经存在！", 'err')
            return redirect(url_for("admin.tag_add"))
        tag = Tag(
            name=data['name']
        )
        db.session.add(tag)
        db.session.commit()
        flash("添加标签成功！", 'ok')
        return redirect(url_for("admin.tag_add"))
    return render_template('admin/tag_add.html', form=form)


# 标签列表
@admins.route("/tag/list/<int:page>/", methods=['GET'])
@admin_login_req
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/tag_list.html', page_data=page_data)


# 标签删除
@admins.route("/tag/del/<int:id>/", methods=['GET'])
@admin_login_req
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash("标签删除成功！", 'ok')
    return redirect(url_for("admin.tag_list", page=1))


# 编辑标签
@admins.route("/tag/edit/<int:id>/", methods=['POST', 'GET'])
@admin_login_req
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag.name != data['name'] and tag_count == 1:
            flash("标签已经存在！", 'err')
            return redirect(url_for("admin.tag_edit", id=id))
        tag.name = data['name']
        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功！", 'ok')
        return redirect(url_for("admin.tag_edit", id=id))
    return render_template('admin/tag_edit.html', form=form, tag=tag)


# 标签搜索
@admins.route("/tag/search/<int:page>/")
@admin_login_req
def tag_search(page=None):
    if page is None:
        page = 1
    key = request.args.get('key', "")
    page_data = Tag.query.filter(
        Tag.name.ilike('%' + key + "%")
    ).order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/tag_list.html', page_data=page_data)


# 编辑电影
@admins.route("/movie/add/", methods=['POST', 'GET'])
@admin_login_req
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config["UP_DIR"]+url)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            playnum=0,
            commentnum=0,
            area=data['area'],
            release_time=data['release_time'],
            length=data['length'],
            tag_id=int(data['tag_id'])
        )
        db.session.add(movie)
        db.session.commit()
        flash("电影添加成功！", 'ok')
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_add.html', form=form)


# 电影列表
@admins.route("/tag/list/")
@admin_login_req
def movie_list():
    return render_template('admin/movie_list.html')


# 编辑上映预告
@admins.route("/preview/add/")
@admin_login_req
def preview_add():
    return render_template('admin/preview_add.html')


# 上映预告列表
@admins.route("/preview/list/")
@admin_login_req
def preview_list():
    return render_template('admin/preview_list.html')


# 会员列表
@admins.route("/user/list/")
@admin_login_req
def user_list():
    return render_template('admin/user_list.html')


# 查看会员
@admins.route("/user/view/")
@admin_login_req
def user_view():
    return render_template('admin/user_view.html')


# 评论列表
@admins.route("/comment/list/")
@admin_login_req
def comment_list():
    return render_template('admin/comment_list.html')


# 收藏列表
@admins.route("/moviecol/list/")
@admin_login_req
def moviecol_list():
    return render_template('admin/moviecol_list.html')


# 管理员登录日志列表
@admins.route("/adminloginlog/list/")
@admin_login_req
def adminloginlog_list():
    return render_template('admin/adminloginlog_list.html')


# 会员登录日志列表
@admins.route("/userloginlog/list/")
@admin_login_req
def userloginlog_list():
    return render_template('admin/userloginlog_list.html')


# 操作日志列表
@admins.route("/oplog/list/")
@admin_login_req
def oplog_list():
    return render_template('admin/oplog_list.html')


# 添加角色
@admins.route("/role/add/")
@admin_login_req
def role_add():
    return render_template('admin/role_add.html')


# 角色列表
@admins.route("/role/list/")
@admin_login_req
def role_list():
    return render_template('admin/role_list.html')


# 添加权限
@admins.route("/auth/add/")
@admin_login_req
def auth_add():
    return render_template('admin/auth_add.html')


# 权限列表
@admins.route("/auth/list/")
@admin_login_req
def auth_list():
    return render_template('admin/auth_list.html')


# 添加管理员
@admins.route("/admin/add/")
@admin_login_req
def admin_add():
    return render_template('admin/admin_add.html')


# 管理员列表
@admins.route("/admin/list/")
@admin_login_req
def admin_list():
    return render_template('admin/admin_list.html')
