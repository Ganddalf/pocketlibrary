from book import *


class Library:
    def __init__(self, file=None):
        self.books = []
        self.ID = 1
        self.file = file

    def __len__(self):
        return len(self.books)

    def add_book(self, name, author, category, year, price):
        self.books.append( Book(self.ID, name, author, category, year, price) )
        self.ID += 1

    def print_books(self):
        print("There are your books:")
        for book in self.books:
            print("\t", book)

    def get_data(self):
        data = ""
        for book in self.books:
            data += str(book) + "\n"
        return data




