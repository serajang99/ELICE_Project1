from flask import Blueprint, request, session, jsonify, make_response
from flask_restful import Api, Resource

from math import ceil

from .db_connect import get_db

bp = Blueprint('search', __name__, url_prefix='/search')
api = Api(bp)


class Search(Resource):
    def get(self):
        q = request.args.get('q', None)
        type = request.args.get('type', None)

        db = get_db()
        cursor = db.cursor()

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
            # print(q)
            return jsonify(result=[])
        else:
            # limit = 8

            # 센터명으로 검색
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
                cursor.execute(
                    f'SELECT * FROM book WHERE title LIKE "%{q}%" ORDER BY id'
                )
            elif type == 'author':
                # cursor.execute(
                #     f"SELECT COUNT(*) As count FROM center WHERE full_address LIKE '%{q}%'"
                # )
                # totalPage = ceil(int(cursor.fetchone()['count']) / 10)
                # if totalPage == 0:
                #     page = 1
                #     totalPage = 1
                # elif page >= totalPage:
                #     page = totalPage

                # offset = (page - 1) * limit

                cursor.execute(
                    f'SELECT * FROM book WHERE author LIKE "%{q}%" ORDER BY id'
                )
            elif type == 'publisher':
                cursor.execute(
                    f'SELECT * FROM book WHERE publisher LIKE "%{q}%" ORDER BY id'
                )
            result = cursor.fetchall()
            # print(result)
        return jsonify(result=result)


api.add_resource(Search, '/books')
