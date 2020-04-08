
class Book:
    def __init__(self, *args):
        self.ID, self.name, self.author, self.category, self.year, self.price = (args)

    def __str__(self):
        return ' | '.join([str(x) for x in [self.ID, self.name, self.author, self.category, self.year, self.price]])

    def edit(self, *args):
        self.ID, self.name, self.author, self.category, self.year, self.price = (args)

    def get(self):
        return (self.ID, self.name, self.author, self.category, self.year, self.price)