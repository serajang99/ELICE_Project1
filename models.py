from db_connect import db


class Book(db.Model):

    __tablename__ = 'book'

    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_date = db.Column(db.String(20), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    description = db.Column(db.TEXT, nullable=False)
    link = db.Column(db.TEXT, nullable=False)
    img = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=5)
    star = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, data):
        if type(data) is dict:
            self.title = data['title']
            self.publisher = data['publisher']
            self.author = data['author']
            self.publication_date = data['publication_date']
            self.pages = data['pages']
            self.isbn = data['isbn']
            self.description = data['description']
            self.link = data['link']
            self.img = data['img']

    def __str__(self):
        return f'{self.title}\n{self.author}\n'


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.TEXT, nullable=False)
    admin = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, username, email, password, admin):
        self.username = username
        self.email = email
        self.password = password
        self.admin = admin

    def __str__(self):
        return f'{self.email}\n'


class BookReview(db.Model):
    __tablename__ = 'BookReview'

    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    comment_date = db.Column(db.DateTime, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    comment = db.Column(db.TEXT, nullable=False)
    star = db.Column(db.Integer, nullable=False)

    def __init__(self, comment_date, user_id, book_id, comment, star):
        self.comment_date = comment_date
        self.user_id = user_id
        self.book_id = book_id
        self.comment = comment
        self.star = star


class BookRental(db.Model):
    __tablename__ = 'BookRental'

    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    rental_date = db.Column(db.DateTime, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    is_returned = db.Column(db.Integer, nullable=False, default=False)
    return_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, rental_date, user_id, book_id, is_returned, return_date):
        self.rental_date = rental_date
        self.user_id = user_id
        self.book_id = book_id
        self.is_returned = is_returned
        self.return_date = return_date


class NewBook(db.Model):

    __tablename__ = 'NewBook'

    id = db.Column(db.Integer, nullable=False,
                   primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __init__(self, title, publisher, author):
        self.title = title
        self.publisher = publisher
        self.author = author
