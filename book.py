# coding: utf8


class Book:
    def __init__(self, id, name, author, category, year, price):
        self.ID = int(id)
        self.name = name
        self.author = author
        self.category = category
        self.year = int(year)
        self.price = int(price)

    def __str__(self):
        return ' | '.join([str(x) for x in [self.ID, self.name,
                                            self.author, self.category,
                                            self.year, self.price]])

    def edit(self, id, name, author, category, year, price):
        self.ID = int(id)
        self.name = name
        self.author = author
        self.category = category
        self.year = int(year)
        self.price = int(price)

    def get(self):
        return self.ID, self.name, self.author, self.category,\
               self.year, self.changed_price(self.price)

    @staticmethod
    def changed_price(price):
        price = list(str(price))
        i = 0
        temp_price = ""
        for char in list(reversed(price)):
            temp_price += char
            i += 1
            if i % 3 == 0:
                temp_price += ' '
        price = ''.join(list(reversed(temp_price))) + " руб."
        return price
