from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from db_connect import db
from datetime import datetime
from models import User, Book, BookReview

bp = Blueprint("book", __name__, url_prefix="/book")


@bp.route('/list/<id>', methods=('GET', 'POST'))
def list(id):
    book = Book.query.filter(Book.id == id)
    print(book)

    if request.method == 'POST':

        message, messageType = None, None
        star = int(request.form['rating'])
        comment = request.form['comment']

        user = User.query.filter(User.email == session['email']).first()
        user_id = user.id

        if comment is None:
            message, messageType = '댓글이 유효하지 않습니다.', 'danger'
        elif star is None:
            message, messageType = '별점이 유효하지 않습니다.', 'danger'
        else:
            review = BookReview(datetime.now(), user_id, id, comment, star)
            db.session.add(review)
            db.session.commit()

            book_reviews = BookReview.query(star).filter(
                BookReview.book_id == id).all()
            print(book_reviews)

            book_star = Book.query(star).filter(Book.book_id == id).first()
            print(book_star)
            db.session.commit()

        flash(message=message, category=messageType)

    return render_template('book.html', book=book)
