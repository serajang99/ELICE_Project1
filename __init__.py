from flask import Flask, render_template, request, g, session
from db_connect import db
from models import Book
import update_data_library
import auth
import book
import search
import rent
import manage
from datetime import datetime


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/elice_library'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(auth.bp)
    app.register_blueprint(book.bp)
    app.register_blueprint(rent.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(manage.bp)

    db.init_app(app)

    @app.route('/')
    def index():

        libraries = update_data_library.update_data_library()

        page = request.args.get('page', type=int, default=1)  # 페이지

        bookList = Book.query.order_by(Book.id.asc())
        bookList = bookList.paginate(page, per_page=8)

        return render_template('index_list.html', books=bookList, libraries=libraries)

    @app.route('/popup')
    def popup():
        session['cnt'] = 1
        day = datetime.today().day - 3
        today = datetime.today().strftime("%Y-%m-")+str(day)+" 00:00:00"
        bookList = Book.query.filter(
            Book.register_time >= today).all()

        return render_template('popup.html', books=bookList)

    return app
