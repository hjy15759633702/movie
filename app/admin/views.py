#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 15:02
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：管理员视图

from . import admins
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import LoginForm, TagForm, MovieForm, PreviewForm
from app.models import Admin, Tag, Movie, Preview, User
from functools import wraps
from app import db, app
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


# 删除某个文件夹
def file_del(filename):
    if filename is not None and filename != "" and os.path.exists(app.config["UP_DIR"]):
        file_path = os.path.join(app.config["UP_DIR"], filename)
        if os.path.exists(file_path):
            os.remove(file_path)


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


# 添加电影
@admins.route("/movie/add/", methods=['POST', 'GET'])
@admin_login_req
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        file_url = str(form.url.data.filename)
        file_logo = str(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR_MOVIE"]):
            os.makedirs(app.config["UP_DIR_MOVIE"])
            os.chmod(app.config["UP_DIR_MOVIE"], "rw")

        if not os.path.exists(app.config["UP_DIR_MOVIE_IMG"]):
            os.makedirs(app.config["UP_DIR_MOVIE_IMG"])
            os.chmod(app.config["UP_DIR_MOVIE_IMG"], "rw")

        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config["UP_DIR_MOVIE"] + url)
        form.logo.data.save(app.config["UP_DIR_MOVIE_IMG"] + logo)
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
@admins.route("/movie/list/<int:page>/", methods=['GET'])
@admin_login_req
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag).filter(
        Movie.tag_id == Tag.id,
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/movie_list.html', page_data=page_data)


# 电影删除
@admins.route("/movie/del/<int:id>/", methods=['GET'])
@admin_login_req
def movie_del(id=None):
    movie = Movie.query.filter_by(id=id).first_or_404()
    db.session.delete(movie)
    db.session.commit()
    # 删除文件
    file_del(movie.url)
    file_del(movie.logo)
    flash("电影删除成功！", 'ok')
    return redirect(url_for("admin.movie_list", page=1))


# 编辑电影
@admins.route("/movie/edit/<int:id>/", methods=['POST', 'GET'])
@admin_login_req
def movie_edit(id=None):
    form = MovieForm()
    # 编辑之前url，logo是存在的，所以不做过滤。
    form.url.validators = []
    form.logo.validators = []
    movie = Movie.query.get_or_404(int(id))
    if request.method == 'GET':
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star
    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title=data['title']).count()
        if movie_count == 1 and movie.title != data['title']:
            flash("电影片名已经存在！", 'err')
            return redirect(url_for("admin.movie_edit", id=id))

        # 判断文件并且创建文件
        if not os.path.exists(app.config["UP_DIR_MOVIE"]):
            os.makedirs(app.config["UP_DIR_MOVIE"])
            os.chmod(app.config["UP_DIR_MOVIE"], "rw")

        if not os.path.exists(app.config["UP_DIR_MOVIE_IMG"]):
            os.makedirs(app.config["UP_DIR_MOVIE_IMG"])
            os.chmod(app.config["UP_DIR_MOVIE_IMG"], "rw")

        if form.url.data != "":
            file_url = str(form.url.data.filename)
            # 删除原来资源
            file_del(movie.url)
            movie.url = change_filename(file_url)
            form.url.data.save(app.config["UP_DIR_MOVIE"] + movie.url)

        if form.logo.data != "":
            file_logo = str(form.logo.data.filename)
            # 删除原来资源
            file_del(movie.logo)
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR_MOVIE_IMG"] + movie.logo)

        movie.title = data['title']
        movie.tag_id = int(data['tag_id'])
        movie.star = int(data['star'])
        movie.info = data['info']
        movie.area = data['area']
        movie.release_time = data['release_time']
        movie.length = data['length']
        db.session.add(movie)
        db.session.commit()
        flash("编辑电影成功！", 'ok')
        return redirect(url_for("admin.movie_edit", id=id))
    return render_template('admin/movie_edit.html', form=form, movie=movie)


# 电影搜索
@admins.route("/movie/search/<int:page>/", methods=['GET'])
@admin_login_req
def movie_search(page=None):
    if page is None:
        page = 1
    key = request.args.get('key', "")
    page_data = Movie.query.join(Tag).filter(
        Movie.tag_id == Tag.id,
        Movie.title.ilike('%' + key + "%")
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/movie_list.html', page_data=page_data)


# 添加上映预告
@admins.route("/preview/add/", methods=['POST', 'GET'])
@admin_login_req
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        file_logo = str(form.logo.data.filename)

        if not os.path.exists(app.config["UP_DIR_PREVIEW"]):
            os.makedirs(app.config["UP_DIR_PREVIEW"])
            os.chmod(app.config["UP_DIR_PREVIEW"], "rw")

        logo = change_filename(file_logo)
        form.logo.data.save(app.config["UP_DIR_PREVIEW"] + logo)
        preview = Preview(
            logo=logo,
            title=data['title']
        )
        db.session.add(preview)
        db.session.commit()
        flash("电影上映预告添加成功！", 'ok')
        return redirect(url_for('admin.preview_add'))
    return render_template('admin/preview_add.html', form=form)


# 上映预告列表
@admins.route("/preview/list/<int:page>/", methods=['GET'])
@admin_login_req
def preview_list(page=None):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(
        Preview.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/preview_list.html', page_data=page_data)


# 上映预告搜索
@admins.route("/preview/search/<int:page>/", methods=['GET'])
@admin_login_req
def preview_search(page=None):
    if page is None:
        page = 1
    key = request.args.get('key', "")
    page_data = Preview.query.filter(
        Preview.title.ilike('%' + key + "%")
    ).order_by(
        Preview.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/preview_list.html', page_data=page_data)


# 上映预告删除
@admins.route("/preview/del/<int:id>/", methods=['GET'])
@admin_login_req
def preview_del(id=None):
    preview = Preview.query.filter_by(id=id).first_or_404()
    db.session.delete(preview)
    db.session.commit()
    # 删除文件
    file_del(preview.logo)
    flash("电影上映预告删除成功！", 'ok')
    return redirect(url_for("admin.preview_list", page=1))


# 编辑上映预告
@admins.route("/preview/edit/<int:id>/", methods=['POST', 'GET'])
@admin_login_req
def preview_edit(id=None):
    form = PreviewForm()
    # 编辑之前logo是存在的，所以不做过滤。
    form.logo.validators = []
    preview = Preview.query.get_or_404(int(id))
    if form.validate_on_submit():
        data = form.data
        preview_count = Preview.query.filter_by(title=data['title']).count()
        if preview_count == 1 and preview.title != data['title']:
            flash("预告标题已经存在！", 'err')
            return redirect(url_for("admin.preview_edit", id=id))

        # 判断文件并且创建文件
        if not os.path.exists(app.config["UP_DIR_PREVIEW"]):
            os.makedirs(app.config["UP_DIR_PREVIEW"])
            os.chmod(app.config["UP_DIR_PREVIEW"], "rw")

        if form.logo.data != "":
            file_logo = str(form.logo.data.filename)
            # 删除原来资源
            file_del(preview.logo)
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR_PREVIEW"] + preview.logo)

        preview.title = data['title']
        db.session.add(preview)
        db.session.commit()
        flash("编辑电影上映预告成功！", 'ok')
        return redirect(url_for("admin.preview_edit", id=id))
    return render_template('admin/preview_edit.html', form=form, preview=preview)


# 会员列表
@admins.route("/user/list/<int:page>/", methods=['GET'])
@admin_login_req
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/user_list.html', page_data=page_data)


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
