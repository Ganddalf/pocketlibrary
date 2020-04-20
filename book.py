# coding: utf8


class Book:
    def __init__(self, id, name, author, category, year, price, file):
        self.ID = int(id)
        self.name = name
        self.author = author
        self.category = category
        self.year = int(year)
        self.price = int(price)
        if not file:
            self.is_path_exist = False
            self.path = ""
        else:
            self.is_path_exist = True
            self.path = file

    def __str__(self):
        return ' | '.join([str(x) for x in [self.ID, self.name,
                                            self.author, self.category,
                                            self.year, self.price,
                                            self.path]])

    def edit(self, id, name, author, category, year, price):
        self.ID = int(id)
        self.name = name
        self.author = author
        self.category = category
        self.year = int(year)
        self.price = int(price)

    def add_file(self, file):
        self.path = file
        self.is_path_exist = True

    def get(self):
        if self.is_path_exist:
            file_status = "Есть"
        else:
            file_status = "-"
        return self.ID, self.name, self.author, self.category, \
               self.year, self.changed_price(self.price), file_status

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
