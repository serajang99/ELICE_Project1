from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g

from db_connect import db
from datetime import datetime
from models import User, Book, BookReview, BookRental, NewBook

bp = Blueprint("book", __name__, url_prefix="/book")


@bp.route('/list/<id>', methods=('GET', 'POST'))
def list(id):
    book = Book.query.filter(Book.id == id).first()

    if request.method == 'POST':
        message, messageType = None, None
        try:
            star = int(request.form['rating'])
        except:
            star = None
        comment = request.form['comment']

        if session.get('email') is not None:
            user = User.query.filter(User.email == session['email']).first()
            user_id = user.id
            review_permission = BookRental.query.filter(
                (BookRental.book_id == id) & (BookRental.user_id == user_id)).first()

            if review_permission is None:
                message, messageType = '대여한 책이 아닙니다.', 'danger'
                reviews = BookReview.query.filter(BookReview.book_id == id).order_by(
                    BookReview.comment_date.desc()).all()
                flash(message=message, category=messageType)
                return render_template('book.html', book=book, reviews=reviews)

        else:
            message, messageType = '로그인이 필요한 기능입니다.', 'danger'
            reviews = BookReview.query.filter(BookReview.book_id == id).order_by(
                BookReview.comment_date.desc()).all()
            flash(message=message, category=messageType)
            return render_template('book.html', book=book, reviews=reviews)

        if comment == "":
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
            for book_star in book_stars:
                cnt += 1
                sum += int(book_star.star)

            book_change_star = Book.query.filter(Book.id == id).first()
            book_change_star.star = round(sum/cnt, 0)
            db.session.commit()

        flash(message=message, category=messageType)

    reviews = BookReview.query.filter(BookReview.book_id == id).order_by(
        BookReview.comment_date.desc()).all()

    return render_template('book.html', book=book, reviews=reviews)


@bp.route('/new', methods=('GET', 'POST'))
def new():
    if request.method == 'GET':
        return render_template('newbook.html')

    elif request.method == 'POST':
        title = request.form.get('title', None)
        author = request.form.get('author', None)
        publisher = request.form.get('publisher', None)
        user = User.query.filter(User.email == session['email']).first()
        user_id = user.id

        # 뉴북 테이블에 추가
        book = NewBook(title, author, publisher, user_id)
        db.session.add(book)
        db.session.commit()
        message = '성공적으로 저장되었습니다.'
        messageType = 'success'
        flash(message=message, category=messageType)

        user = User.query.filter(User.email == session['email']).first()
        user_id = user.id
        bookreviews = BookReview.query.filter(
            BookReview.user_id == user_id).all()
        reviews = []
        for bookreview in bookreviews:
            book = Book.query.filter(Book.id == bookreview.book_id).first()
            reviews.append((bookreview, book))

        newbooks = NewBook.query.filter(NewBook.user_id == user_id).all()
        return render_template('mypage.html', reviews=reviews, newbooks=newbooks, user=user)
