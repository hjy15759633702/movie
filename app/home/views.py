#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2018/3/10 15:02
# @Author    : hjy     
# @Software  ：PyCharm
# @Detial    ：前台视图

from . import homes
from flask import render_template, redirect, url_for, flash, session, request
from app.home.forms import RegistForm, LoginForm, UserdetialForm, PwdForm, CommentForm
from app.models import User, Preview, Userlog, Comment, Movie, Moviecol, Tag
from app import db, app
import uuid
from werkzeug.security import generate_password_hash
from functools import wraps
import os
import datetime
import json


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


# 验证是否处于登录
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 列表
@homes.route("/")
def index():
    tags = Tag.query.all()
    page_data = Movie.query

    tid = request.args.get("tid", 0)
    if int(tid) != 0:
        page_data = page_data.filter_by(tag_id=int(tid))

    star = request.args.get("star", 0)
    if int(star) != 0:
        page_data = page_data.filter_by(star=int(star))

    time = request.args.get("time", 0)
    if int(time) != 0:
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.addtime.asc()
            )

    pm = request.args.get("pm", 0)
    if int(pm) != 0:
        if int(pm) == 1:
            page_data = page_data.order_by(
                Movie.playnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.playnum.asc()
            )

    cm = request.args.get("cm", 0)
    if int(cm) != 0:
        if int(cm) == 1:
            page_data = page_data.order_by(
                Movie.commentnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.commentnum.asc()
            )
    page = request.args.get("page", 1)
    page_data = page_data.paginate(page=int(page), per_page=10)
    p = dict(
        tid=tid,
        star=star,
        time=time,
        pm=pm,
        cm=cm
    )
    return render_template('home/index.html', tags=tags, p=p, page_data=page_data, page_count=len(page_data.items))


# 登录
@homes.route("/login/", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()

        if not user:
            flash("账号不存在！", 'err')
            return redirect(url_for("home.login"))

        if not user.check_pwd(data['pwd']):
            flash("密码错误！", 'err')
            return redirect(url_for("home.login"))

        # 账号冻结
        if not user.status == 0:
            flash("该账号已经被冻结了，请联系客服！", 'err')
            return redirect(url_for("home.login"))

        session['user'] = data['name']
        session['user_id'] = user.id
        session['user_face'] = user.face
        userlog = Userlog(
            user_id=session['user_id'],
            ip=request.remote_addr,
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(request.args.get('next') or url_for("home.user"))
    return render_template('home/login.html', form=form)


# 退出
@homes.route("/logout/")
@user_login_req
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('home.login'))


# 注册
@homes.route("/regist/", methods=['POST', 'GET'])
def regist():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            pwd=generate_password_hash(data['pwd']),
            email=data['email'],
            phone=data['phone'],
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash("会员注册成功！", 'ok')
        return redirect(url_for("home.regist"))
    return render_template('home/regist.html', form=form)


# 会员中心
@homes.route("/user/", methods=['POST', 'GET'])
@user_login_req
def user():
    form = UserdetialForm()
    user = User.query.get_or_404(int(session['user_id']))
    form.face.validators = []
    if request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data

        name_count = User.query.filter_by(name=data['name']).count()
        if name_count == 1 and user.name != data['name']:
            flash("用户昵称已经存在！", 'err')
            return redirect(url_for("home.user"))

        email_count = User.query.filter_by(email=data['email']).count()
        if email_count == 1 and user.email != data['email']:
            flash("邮箱已经存在！", 'err')
            return redirect(url_for("home.user"))

        phone_count = User.query.filter_by(phone=data['phone']).count()
        if phone_count == 1 and user.phone != data['phone']:
            flash("手机号码已经存在！", 'err')
            return redirect(url_for("home.user"))

        if not os.path.exists(app.config["UP_DIR_HEAD"]):
            os.makedirs(app.config["UP_DIR_HEAD"])
            os.chmod(app.config["UP_DIR_HEAD"], "rw")

        if form.face.data != "":
            file_face = str(form.face.data)
            # 删除原来资源
            # file_del(app.config["UP_DIR_MOVIE_IMG"], movie.logo)
            user.face = change_filename(file_face)
            form.face.data.save(app.config["UP_DIR_HEAD"] + user.face)

        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']
        db.session.add(user)
        db.session.commit()
        flash("会员信息修改成功！", 'ok')
        return redirect(url_for("home.user"))
    return render_template('home/user.html', form=form, user=user)


# 修改密码
@homes.route("/pwd/", methods=['POST', 'GET'])
@user_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(
            name=session["user"]
        ).first()
        from werkzeug.security import generate_password_hash
        user.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(user)
        db.session.commit()
        flash("修改密码成功，请重新登录！", 'ok')
        return redirect(url_for("home.login"))

    return render_template('home/pwd.html', form=form)


# 评论
@homes.route("/comments/", methods=['GET'])
def comments(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id,
        User.id == session['user_id']
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/comments.html', page_data=page_data)


# 登录日志
@homes.route("/loginlog/<int:page>", methods=['GET'])
@user_login_req
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.join(User).filter(
        User.id == Userlog.user_id,
        User.id == session['user_id']
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/loginlog.html', page_data=page_data)


# 电影收藏
@homes.route("/moviecol/<int:page>/")
@user_login_req
def moviecol(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(Movie).join(User).filter(
        Movie.id == Moviecol.movie_id,
        User.id == Moviecol.user_id,
        User.id == session['user_id']
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/moviecol.html', page_data=page_data)


# 添加电影收藏
@homes.route("/moviecol/add/", methods=['GET'])
@user_login_req
def moviecol_add():
    mid = request.args.get('mid', '')
    uid = request.args.get('uid', '')
    movelcol_count = Moviecol.query.filter(
        db.and_(Moviecol.user_id == int(uid), Moviecol.movie_id == int(mid))
    ).count()
    if movelcol_count == 1:
        data = dict(ok=0)
    if movelcol_count == 0:
        moviecol = Moviecol(
            user_id=int(uid),
            movie_id=int(mid)
        )
        db.session.add(moviecol)
        db.session.commit()
        data = dict(ok=1)
    return json.dumps(data)


# 上映预告
@homes.route("/animation/")
def animation():
    previews = Preview.query.all()
    return render_template('home/animation.html', previews=previews)


# 搜索
@homes.route("/search/<int:page>/", methods=['GET'])
def search(page=None):
    if page is None:
        page = 1
    key = request.args.get('key', "")
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id,
        Movie.title.ilike('%' + key + "%")
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    page_data.key = key
    return render_template('home/search.html', movie_count=len(page_data.items), page_data=page_data, key=key)


# 电影播放
@homes.route("/play/<int:id>/<int:page>/", methods=['GET', 'POST'])
def play(id=None, page=1):
    movie = Movie.query.get_or_404(int(id))
    form = CommentForm()
    movie.playnum = movie.playnum + 1

    if page is None:
        page = 1
    page_data = Comment.query.join(Movie).join(User).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)

    if 'user' in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data['comment'],
            movie_id=movie.id,
            user_id=session['user_id']
        )
        db.session.add(comment)
        db.session.commit()
        movie.commentnum = movie.commentnum + 1
        flash("评论成功！", 'ok')
        return redirect(url_for("home.play", id=movie.id, page=page))
    db.session.add(movie)
    db.session.commit()
    return render_template('home/play.html', movie=movie, form=form, page_data=page_data)
