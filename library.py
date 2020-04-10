# coding: utf8
from book import *
from operator import attrgetter


class Library:
    def __init__(self):
        self.books = []
        self.ID = 1
        self.file = None
        self.changed = False

    def __len__(self):
        return len(self.books)

    def add_book(self, name, author, category, year, price):
        self.books.append(Book(self.ID, name, author, category, year, price))
        self.ID += 1

    def load_book(self, id, name, author, category, year, price):
        self.books.append(Book(id, name, author, category, year, price))

    def print_books(self):
        print("There are your books:")
        for book in self.books:
            print("\t", book)

    def get_data(self):
        data = ""
        self.books.sort(key=attrgetter("ID"), reverse=False)
        for book in self.books:
            data += str(book) + "\n"
        return data

    def clear(self):
        self.ID = 1
        self.file = None
        self.books.clear()
        self.changed = False

    def set_data(self, data):
        try:
            data  = data.split('\n')
            data.pop()
            data = [str.split(' | ') for str in data]
            for book_data in data:
                self.load_book(book_data[0], book_data[1], book_data[2],
                               book_data[3], book_data[4], book_data[5])
                self.ID = int(self.books[-1].ID) + 1
        except:
            self.clear()
            return False

        return True

    def sort_by_attribute(self, attr):
        if self.books == sorted(self.books, key=attrgetter(attr),
                                reverse=False):
            self.books.sort(key=attrgetter(attr), reverse=True)
        else:
            self.books.sort(key=attrgetter(attr), reverse=False)
