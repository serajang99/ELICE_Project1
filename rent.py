from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from db_connect import get_db
from datetime import datetime

bp = Blueprint("rent", __name__, url_prefix="/rent")


@bp.route('/list', methods=('GET', 'POST'))
def list():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT id FROM user WHERE email = %s',
                   (session['email']))
    user_id = cursor.fetchone()

    cursor.execute(
        f'SELECT book_id FROM bookRental WHERE user_id = %s', (user_id['id'])
    )
    book_id = cursor.fetchall()
    print(book_id)
    books = []
    for id in book_id:
        cursor.execute(
            f'SELECT * FROM book WHERE id = %s', (id['book_id'])
        )
        books.append(cursor.fetchone())

    print(books)
    return render_template('rent_list.html', books=books)


@bp.route('/ret/<id>', methods=('GET', 'POST'))
def ret(id):

    if id == '-1':
        db = get_db()
        cursor = db.cursor()

        cursor.execute('SELECT id FROM user WHERE email = %s',
                       (session['email']))
        user_id = cursor.fetchone()

        cursor.execute(
            f'SELECT book_id FROM bookRental WHERE user_id = %s', (
                user_id['id'])
        )
        book_ids = cursor.fetchall()
        # print(book_id)
        books = []
        for book_id in book_ids:
            cursor.execute(
                f'SELECT * FROM book WHERE id = %s', (book_id['book_id'])
            )
            books.append(cursor.fetchone())

        # print(books)
        return render_template('rent_ret.html', books=books)

    else:
        db = get_db()
        cursor = db.cursor()

        cursor.execute('SELECT id FROM user WHERE email = %s',
                       (session['email']))
        user_id = cursor.fetchone()['id']
        print(user_id)

        cursor.execute(
            f'DELETE FROM bookRental WHERE book_id = %s', (id)
        )
        db.commit()

        cursor.execute(
            f'UPDATE book SET stock=stock+1 WHERE id=%s', (id)
        )
        db.commit()

        return redirect('/rent/list')


@bp.route('/rent/<id>', methods=('GET', 'POST'))
def rent(id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT id FROM user WHERE email = %s',
                   (session['email']))
    user_id = cursor.fetchone()
    book_id = id

    print(user_id, book_id)

    cursor.execute(
        'SELECT stock FROM book WHERE id=%s', (book_id)
    )
    stock = cursor.fetchone()

    if stock['stock'] == 0:
        message, messageType = '책이 존재하지 않습니다.', 'danger'
        flash(message=message, category=messageType)
    else:
        cursor.execute(
            'INSERT INTO bookRental (rental_date, user_id, book_id) VALUES (%s, %s, %s)',
            (datetime.now(), user_id['id'], book_id)
        )
        db.commit()

        cursor.execute(
            'UPDATE book SET stock=stock-1 WHERE id=%s', (book_id)
        )
        db.commit()

    return redirect('/')
