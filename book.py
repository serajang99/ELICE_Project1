from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from db_connect import get_db
import re

bp = Blueprint("book", __name__, url_prefix="/book")


@bp.route('/list/<id>', methods=('GET', 'POST'))
def list(id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM book WHERE id = %s' % id)
    book = cursor.fetchone()

    if request.method == 'POST':

        message, messageType = None, None
        star = int(request.form['rating'])
        comment = request.form['comment']
        cursor.execute('SELECT id FROM user WHERE email = %s',
                       (session['email']))
        user_id = cursor.fetchone()
        print(star, comment, user_id, id)

        if comment is None:
            message, messageType = '댓글이 유효하지 않습니다.', 'danger'
        else:
            cursor.execute(
                'INSERT INTO bookReview (user_id, book_id, comment, star) VALUES (%s, %s, %s, %s)',
                (user_id['id'], id, comment, star)
            )
            db.commit()

        flash(message=message, category=messageType)

    db.close()
    return render_template('book.html', book=book)
