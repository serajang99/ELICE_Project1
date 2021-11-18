from flask import Blueprint, request, session, jsonify, make_response
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

        # # 권한 체크
        # username = session.get('username', None)
        # if username is None:
        #     return make_response(jsonify(message='로그인을 해주세요.'), 401)
        # else:
        #     cursor.execute(
        #         'SELECT p_search FROM permission WHERE username = %s;', (
        #             username, )
        #     )
        #     perm = cursor.fetchone()

        #     if perm is None or perm['p_search'] == 0:
        #         return make_response(jsonify(message='검색 권한이 없습니다.'), 403)

        if q is None:
            return jsonify(result=[])
        else:
            # limit = 8

            if type == 'title':
                # cursor.execute(
                #     f"SELECT COUNT(*) As count FROM book WHERE title LIKE '%{q}%'"
                # )
                # totalPage = ceil(int(cursor.fetchone()['count']) / 10)
                # if totalPage == 0:
                #     page = 1
                #     totalPage = 1
                # elif page >= totalPage:
                #     page = totalPage

                # offset = (page - 1) * limit

                search_books = Book.query.filter(
                    Book.title.like(f"%{q}%")).order_by(Book.id).all()
            elif type == 'author':
                search_books = Book.query.filter(
                    Book.author.like(f"%{q}%")).order_by(Book.id).all()
            elif type == 'publisher':
                search_books = Book.query.filter(
                    Book.publisher.like(f"%{q}%")).order_by(Book.id).all()

        return jsonify(result=search_books)


api.add_resource(Search, '/books')
