from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

import re

from models import User, BookReview, Book
from db_connect import db

bp = Blueprint("manage", __name__, url_prefix="/manage")


@bp.route('/user', methods=('GET', 'POST'))
def user():
    users = User.query.filter(User.admin == 0).all()
    admins = User.query.filter(User.admin == 1).all()

    if request.method == 'GET':
        return render_template('manageuser.html', users=users, admins=admins)
    elif request.method == 'POST':
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
            user = User(username, email, generate_password_hash(password), 1)

            db.session.add(user)
            db.session.commit()

        flash(message=message, category=messageType)

    return render_template('manageuser.html', users=users, admins=admins)


@bp.route('/book', methods=('GET', 'POST'))
def book():
    books = Book.query.all()
    if request.method == 'GET':
        return render_template('managebook.html', books=books)
    elif request.method == 'POST':

        return render_template('managebook.html', books=books)
