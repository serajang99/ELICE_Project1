from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

import re

from models import User, BookReview, Book
from db_connect import db

bp = Blueprint("auth", __name__, url_prefix="/user")


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form.get('username', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        password2 = request.form.get('password2', None)

        message, messageType = None, None

        check_email = re.compile(
            '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        check_name = re.compile(
            '^[가-힣a-zA-Z]+$')
        check_pw1 = re.compile(
            '^(?=.*[a-zA-z])(?=.*[0-9])(?=.*[~!@#$%^&*+=-]).{8,100}$')

        check_pw2 = re.compile('^[a-zA-Z\d]{10,100}$')
        check_pw3 = re.compile('^[a-zA-Z~!@#$%^&*]{10,100}$')
        check_pw4 = re.compile('^[\d~!@#$%^&*]{10,100}$')

        if username is None or check_name.match(username) is None:
            message, messageType = '이름이 유효하지 않습니다.', 'danger'
        elif email is None or check_email.match(email) is None:
            message, messageType = '아이디가 유효하지 않습니다.', 'danger'
        elif password is None or (check_pw1.match(password) or check_pw2.match(password) or check_pw3.match(password) or check_pw4.match(password)) is None:
            message, messageType = '비밀번호는 영문/숫자/특수문자(~!@#$%^&*) 3개 조합 8자리 혹은 2개 조합 10자리 이상으로 입력해주세요.', 'danger'
        elif password != password2:
            message, messageType = '비밀번호를 다시 확인해주십시오.', 'danger'
        else:
            user = User.query.filter(User.email == email).first()

            if user is not None:
                message, messageType = f'{username} 계정은 이미 등록된 계정입니다.', 'warning'

        if message is None:
            # 유저 테이블에 추가
            user = User(username, email, generate_password_hash(password), 0)

            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.signin'))

        flash(message=message, category=messageType)

    return render_template('signup.html')


@bp.route('/signin', methods=('GET', 'POST'))
def signin():
    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        message, messageType = None, None

        user = User.query.filter(User.email == email).first()
        print(user, email, password)

        if user is None:
            message, messageType = '등록되지 않은 계정입니다.', 'danger'
        elif not check_password_hash(user.password, password):
            message, messageType = '비밀번호가 틀렸습니다.', 'danger'
        elif len(password) < 8:
            message, messageType = '비밀번호가 8자리 이상이어야 합니다.', 'danger'

        if message is None:
            session.clear()
            session['email'] = user.email
            session['admin'] = user.admin
            return redirect(url_for('index'))

        flash(message=message, category=messageType)

    return render_template('signin.html')


@bp.before_app_request
def load_logged_in_user():
    email = session.get('email')
    admin = session.get('admin')
    g.email = None if email is None else email
    g.admin = None if admin is None else admin


@bp.route('/signout')
def signout():
    session.clear()
    return redirect(url_for('index'))


@bp.route('/mypage', methods=('GET', 'POST'))
def mypage():
    user = User.query.filter(User.email == session['email']).first()
    user_id = user.id
    bookreviews = BookReview.query.filter(BookReview.user_id == user_id).all()
    reviews = []
    for bookreview in bookreviews:
        book = Book.query.filter(Book.id == bookreview.book_id).first()
        reviews.append((bookreview, book))
    return render_template('mypage.html', reviews=reviews)


@bp.route('/adminpage', methods=('GET', 'POST'))
def adminpage():
    return render_template('adminpage.html')
