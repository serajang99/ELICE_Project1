from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from db_connect import db
from models import Book, User, BookRental
from datetime import datetime

bp = Blueprint("rent", __name__, url_prefix="/rent")


@bp.route('/list', methods=('GET', 'POST'))
def list():

    user = User.query.filter(User.email == session['email']).first()
    user_id = user.id

    rented_books = BookRental.query.filter(BookRental.user_id == user_id).all()
    books_ids = []
    for book in rented_books:
        books_ids.append(book.book_id)

    books = []
    for book_id in books_ids:
        book = Book.query.filter(Book.id == book_id).first()
        books.append(book)

    print(books)
    return render_template('rent_list.html', books=books)


@bp.route('/ret/<id>', methods=('GET', 'POST'))
def ret(id):

    user = User.query.filter(User.email == session['email']).first()
    user_id = user.id

    if id == '-1':
        rented_books = BookRental.query.filter(
            BookRental.user_id == user_id).all()
        books_ids = []
        for book in rented_books:
            books_ids.append(book.book_id)

        books = []
        for book_id in books_ids:
            book = Book.query.filter(Book.id == book_id).first()
            books.append(book)
        return render_template('rent_ret.html', books=books)

    else:
        book = BookRental.query.filter(BookRental.book_id == id).first()
        db.session.delete(book)
        db.session.commit()

        book = Book.query.filter(Book.id == id).first()
        book.stock += 1
        db.session.commit()

        return redirect('/rent/list')


@bp.route('/rent/<id>', methods=('GET', 'POST'))
def rent(id):

    user = User.query.filter(User.email == session['email']).first()
    user_id = user.id
    book_id = int(id)

    book = Book.query.filter(Book.id == book_id).first()
    stock = book.stock

    if stock == 0:
        message, messageType = '책이 존재하지 않습니다.', 'danger'
        flash(message=message, category=messageType)
    else:
        book_rental = BookRental(datetime.now(), user_id, book_id)
        db.session.add(book_rental)
        db.session.commit()

        book = Book.query.filter(Book.id == id).first()
        book.stock -= 1
        db.session.commit()

    return redirect('/')
