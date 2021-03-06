from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g

from db_connect import db
from models import Book, User, BookRental
from datetime import datetime
from sqlalchemy.sql.expression import false

bp = Blueprint("rent", __name__, url_prefix="/rent")


@bp.route('/list', methods=('GET', 'POST'))
def list():

    user = User.query.filter(User.email == session['email']).first()
    user_id = user.id

    rented_books = BookRental.query.filter(
        BookRental.user_id == user_id).order_by(BookRental.rental_date.desc()).all()
    books = []
    for rented_book in rented_books:
        book_info = Book.query.filter(Book.id == rented_book.book_id).first()
        books.append((book_info, rented_book))

    print(books)
    if len(books) == 0:
        message, messageType = '대여한 책이 존재하지 않습니다.', 'danger'
        flash(message=message, category=messageType)

    return render_template('rent_list.html', books=books)


@bp.route('/ret/<id>', methods=('GET', 'POST'))
def ret(id):

    message, messageType = None, None
    user = User.query.filter(User.email == session['email']).first()
    user_id = user.id

    if id == '-1':
        rented_books = BookRental.query.filter(
            (BookRental.user_id == user_id) & (BookRental.is_returned == 0)).all()

        books = []
        for book in rented_books:
            book_info = Book.query.filter(Book.id == book.book_id).first()
            books.append(book_info)
        if len(books) == 0:
            message, messageType = '대여한 책이 존재하지 않습니다.', 'danger'
            flash(message=message, category=messageType)
        return render_template('rent_ret.html', books=books)

    else:
        book = BookRental.query.filter((BookRental.book_id == id) & (
            BookRental.user_id == user_id) & (BookRental.is_returned == 0)).first()
        book.is_returned = 1
        book.return_date = datetime.now()
        db.session.commit()

        book = Book.query.filter(Book.id == id).first()
        book.stock += 1
        db.session.commit()

        rented_books = BookRental.query.filter(
            (BookRental.user_id == user_id) & (BookRental.is_returned == 0)).all()

        books = []
        for book in rented_books:
            book_info = Book.query.filter(Book.id == book.book_id).first()
            books.append(book_info)

        if len(books) == 0:
            message, messageType = '대여한 책이 존재하지 않습니다.', 'danger'

        flash(message=message, category=messageType)
        return render_template('rent_ret.html', books=books)


@bp.route('/rent/<id>', methods=('GET', 'POST'))
def rent(id):

    user = User.query.filter(User.email == session['email']).first()
    user_id = user.id
    book_id = int(id)

    book = Book.query.filter(Book.id == book_id).first()
    stock = book.stock

    message, messageType = None, None

    if stock == 0:
        message, messageType = '책이 존재하지 않습니다.', 'danger'
    else:
        book_rental = BookRental(
            datetime.now(), user_id, book_id, 0, datetime.now())
        db.session.add(book_rental)
        db.session.commit()

        book = Book.query.filter(Book.id == id).first()
        book.stock -= 1
        db.session.commit()
        message, messageType = '성공적으로 대여하였습니다.', 'success'

        rent_already = BookRental.query.filter(
            (BookRental.book_id == id) & (BookRental.user_id == user_id) & (BookRental.is_returned == 0)).all()
        if len(rent_already) > 1:
            message, messageType = f'이미 {len(rent_already)-1}권 대여한 책입니다.', 'warning'

    flash(message=message, category=messageType)
    return redirect('/')
