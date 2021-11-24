from flask import Flask, render_template, request
from db_connect import db
from models import Book
from . import update_data
from . import update_data_library
from . import auth
from . import book
from . import search
from . import rent
from . import manage

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

    # update_data.update_data()
    libraries = update_data_library.update_data_library()

    page = request.args.get('page', type=int, default=1)  # 페이지

    bookList = Book.query.order_by(Book.id.asc())
    bookList = bookList.paginate(page, per_page=8)

    return render_template('index.html', books=bookList, libraries=libraries)
