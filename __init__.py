from flask import Flask, render_template
from .db_connect import get_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # from . import update_data
    # update_data.update_data()

    from . import search
    app.register_blueprint(search.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import rent
    app.register_blueprint(rent.bp)
    
    from . import book
    app.register_blueprint(book.bp)

    @app.route('/')
    def index():
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            f'SELECT * FROM book'
        )
        books = cursor.fetchall()
        return render_template('index.html', books=books)

    return app
