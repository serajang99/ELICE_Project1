from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from db_connect import db
from datetime import datetime
from models import User, Book, BookReview

bp = Blueprint("book", __name__, url_prefix="/book")


@bp.route('/list/<id>', methods=('GET', 'POST'))
def list(id):
    book = Book.query.filter(Book.id == id).first()

    if request.method == 'POST':

        message, messageType = None, None
        star = int(request.form['rating'])
        comment = request.form['comment']

        if session.get('email') is not None:
            user = User.query.filter(User.email == session['email']).first()
            user_id = user.id
        else:
            message, messageType = '로그인이 필요한 기능입니다.', 'danger'
            return render_template('book.html', book=book)

        if comment is None:
            message, messageType = '댓글이 유효하지 않습니다.', 'danger'
        elif star is None:
            message, messageType = '별점이 유효하지 않습니다.', 'danger'
        else:
            review = BookReview(datetime.now(), user_id, id, comment, star)
            db.session.add(review)
            db.session.commit()

            book_stars = BookReview.query.filter(
                BookReview.book_id == id).all()

            cnt = 0
            sum = 0
            for star in book_stars:
                cnt += 1
                sum += int(star.star)

            book_change_star = Book.query.filter(Book.id == id).first()
            book_change_star.star = round(sum/cnt)
            db.session.commit()

        flash(message=message, category=messageType)

    reviews = BookReview.query.filter(BookReview.book_id == id).all()

    return render_template('book.html', book=book, reviews=reviews)
