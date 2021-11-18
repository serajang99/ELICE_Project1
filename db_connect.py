# import pymysql

# from flask import g

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# class MysqlPool:
#     def __init__(self):
#         self.conn = pymysql.connect(
#             user='root',
#             passwd='1234',
#             host='localhost',
#             port=3306,
#             db='elice_library',
#             charset='utf8mb4'
#         )

#     def cursor(self):
#         return self.conn.cursor(pymysql.cursors.DictCursor)

#     def commit(self):
#         self.conn.commit()

#     def close(self):
#         self.conn.close()


# def get_db():
#     if 'db' not in g:
#         g.db = MysqlPool()

#     return g.db


# def close_db(e=None):
#     db = g.pop('db', None)

#     if db is not None:
#         db.close()
