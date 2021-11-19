from flask import Flask, render_template
from db_connect import db
from models import Book
from . import update_data
from . import auth
from . import book
from . import search
from . import rent

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='dev',
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/elice_library'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.register_blueprint(auth.bp)
app.register_blueprint(book.bp)
app.register_blueprint(search.bp)
app.register_blueprint(rent.bp)

db.init_app(app)


@app.route('/')
def index():

    # update_data.update_data()

    book_list = Book.query.all()
    return render_template('index.html', books=book_list)
