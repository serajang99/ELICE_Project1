class Book:
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
