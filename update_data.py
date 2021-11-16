import models
import db_connect
import openpyxl
from flask_apscheduler import APScheduler

scheduler = APScheduler()


@scheduler.task('interval', id='update_data', hours=3)
def update_data():
    wb = openpyxl.load_workbook(filename='data/book.xlsx')
    ws = wb.active

    db = db_connect.MysqlPool()
    cursor = db.cursor()

    cursor.execute('TRUNCATE book')
    db.commit()

    query = """INSERT INTO book (title, publisher, author, publication_date, pages, isbn, description, link, img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

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
        img = f'img/book_img/{r-1}.png'
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
        }
        book = models.Book(data)

        values = (book.title, book.publisher, book.author, book.publication_date,
                  book.pages, book.isbn, book.description, book.link, book.img)

        cursor.execute(query, values)
        db.commit()

    print('데이터 저장 완료')

    cursor.close()
