from flask import Blueprint, request, jsonify, render_template
from flask_restful import Api, Resource

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
                    Book.title.like(f"%{q}%")).order_by(Book.id).all()
            elif type == 'author':
                search_books = Book.query.filter(
                    Book.author.like(f"%{q}%")).order_by(Book.id).all()
            elif type == 'publisher':
                search_books = Book.query.filter(
                    Book.publisher.like(f"%{q}%")).order_by(Book.id).all()

            return jsonify(render_template('search.html', books=search_books))


api.add_resource(Search, '/books')
