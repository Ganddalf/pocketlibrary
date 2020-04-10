
class Book:
    def __init__(self, *args):
        self.ID, self.name, self.author, self.category, self.year, self.price = (args)

    def __str__(self):
        return ' | '.join([str(x) for x in [self.ID, self.name, self.author, self.category, self.year, self.price]])

    def edit(self, *args):
        self.ID, self.name, self.author, self.category, self.year, self.price = (args)

    def get(self):
        return (self.ID, self.name, self.author, self.category, self.year, self.changed_price(self.price))

    def changed_price(self, price):
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
