from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from db_connect import get_db
from datetime import datetime

bp = Blueprint("rent", __name__, url_prefix="/rent")


@bp.route('/list', methods=('GET', 'POST'))
def list():
    return render_template('rent.html')


@bp.route('/ret', methods=('GET', 'POST'))
def ret():

    return render_template('rent.html')


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
        'INSERT INTO bookRental (rental_date, user_id, book_id) VALUES (%s, %s, %s)',
        (datetime.now(), user_id['id'], book_id)
    )
    db.commit()

    cursor.execute(
        'UPDATE book SET stock=stock-1 WHERE id=%s', (book_id)
    )
    db.commit()

    return redirect('/')
