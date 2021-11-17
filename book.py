from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from db_connect import get_db
import re

bp = Blueprint("book", __name__, url_prefix="/book")


@bp.route('/list', methods=('GET', 'POST'))
def list():
    return render_template('book.html')
