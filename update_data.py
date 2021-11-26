import openpyxl
from flask_apscheduler import APScheduler
from models import Book
from db_connect import db
import os
import natsort
from datetime import datetime
from flask import Flask

scheduler = APScheduler()


@scheduler.task('interval', id='update_data', seconds=10)
def update_data():
    wb = openpyxl.load_workbook(filename='data/book.xlsx')
    ws = wb.active

    img_dir = os.listdir('./static/img/book_img')
    img_list = natsort.natsorted(img_dir)

    for r in range(2, ws.max_row):

        if ws.cell(r, 2).value is None:
            break

        title = ws.cell(r, 2).value
        publisher = ws.cell(r, 3).value
        author = ws.cell(r, 4).value
        publication_date = ws.cell(r, 5).value
        pages = ws.cell(r, 6).value
        isbn = ws.cell(r, 7).value
        description = ws.cell(r, 8).value
        link = ws.cell(r, 9).value
        img_value = img_list[r-2]
        img = f'img/book_img/{img_value}'
        data = {
            'title': title,
            'publisher': publisher,
            'author': author,
            'publication_date': publication_date,
            'pages': pages,
            'isbn': isbn,
            'description': description,
            'link': link,
            'img': img,
            'register_time': '0000-00-00 00:00:00'
        }
        book = Book(data)

        db.session.add(book)
        db.session.commit()

    print('데이터 저장 완료')
    db.session.close()


def init_scheduler(app):
    scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
)
init_scheduler(app)
