from flask import Blueprint, request, session, flash, redirect, url_for, render_template, g
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from db_connect import get_db
import re

bp = Blueprint("rent", __name__, url_prefix="/rent")


@bp.route('/list', methods=('GET', 'POST'))
def list():
    return render_template('rent.html')


@bp.route('/ret', methods=('GET', 'POST'))
def ret():
    return render_template('rent.html')


@bp.route('/rent', methods=('GET', 'POST'))
def rent():
    return redirect('/')
