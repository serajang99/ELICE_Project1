from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

import re
from datetime import datetime

from models import User, BookReview, Book
from db_connect import db

bp = Blueprint("manage", __name__, url_prefix="/manage")


@bp.route('/user', methods=('GET', 'POST'))
def user():

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
            user = User(username, email, generate_password_hash(password), 1)

            db.session.add(user)
            db.session.commit()

        flash(message=message, category=messageType)

    users = User.query.filter(User.admin == 0).all()
    admins = User.query.filter(User.admin == 1).all()
    return render_template('manageuser.html', users=users, admins=admins)


@bp.route('/book', methods=('GET', 'POST'))
def book():

    if request.method == 'POST':

        title = request.form.get('title')
        publisher = request.form.get('publisher')
        author = request.form.get('author')
        publication_date = request.form.get('publication_date')
        pages = request.form.get('pages')
        isbn = request.form.get('isbn')
        description = request.form.get('description')
        link = request.form.get('link')
        img_value = 0
        img = f'img/book_img/{img_value}.jpg'
        data = {
            'title': title,
            'publisher': publisher,
            'author': author,
            'publication_date': publication_date,
            'pages': pages,
            'isbn': isbn,
            'description': description,
            'link': link,
            'img': img,
            'register_time': datetime.now()
        }
        book = Book(data)

        db.session.add(book)
        db.session.commit()

    books = Book.query.order_by(Book.id.desc()).all()
    return render_template('managebook.html', books=books)
