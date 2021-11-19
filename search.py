from flask import Blueprint, request, session, jsonify, make_response, render_template
from flask_restful import Api, Resource

from math import ceil

from .db_connect import db
from models import Book

bp = Blueprint('search', __name__, url_prefix='/search')
api = Api(bp)


class Search(Resource):
    def get(self):
        q = request.args.get('q', None)
        type = request.args.get('type', None)

        if q is None:
            return jsonify(result=[])
        else:
            if type == 'title':
                search_books = Book.query.filter(
                    Book.title.like(f"%{q}%")).order_by(Book.id)
            elif type == 'author':
                search_books = Book.query.filter(
                    Book.author.like(f"%{q}%")).order_by(Book.id)
            elif type == 'publisher':
                search_books = Book.query.filter(
                    Book.publisher.like(f"%{q}%")).order_by(Book.id)

            page = request.args.get('page', type=int, default=1)  # 페이지
            bookList = search_books.paginate(page, per_page=8)

            return jsonify(render_template('search.html', books=bookList))
    # return jsonify(result=search_books)


api.add_resource(Search, '/books')
