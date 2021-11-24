from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g

from models import User, BookReview, Book
from db_connect import db

bp = Blueprint("manage", __name__, url_prefix="/manage")


@bp.route('/user', methods=('GET', 'POST'))
def user():
    users = User.query.filter(User.admin == 0).all()
    return render_template('manageuser.html', users=users)


@bp.route('/book', methods=('GET', 'POST'))
def book():
    books = Book.query.all()
    return render_template('managebook.html', books=books)
