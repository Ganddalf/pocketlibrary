import tkinter as tk
from tkinter import ttk
from library import *
from book import *

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.lib = lib
        self.init_main()

    def init_main(self):

        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open_add_dialog = tk.Button(toolbar, text='Добавить книгу',command=self.open_add_dialog,
                                        bg="#d7d8e0", bd=0, compound=tk.TOP)
        btn_open_add_dialog.pack(side=tk.LEFT)

        btn_open_update_dialog = tk.Button(toolbar, text='Редактировать данные', command=self.open_update_dialog,
                                        bg="#d7d8e0", bd=0, compound=tk.TOP)
        btn_open_update_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'author', 'category', 'year', 'price'),
                                 height=15, show="headings")
        self.tree.column('ID', width=40, minwidth=40, anchor=tk.CENTER)
        self.tree.column('name', width=200, minwidth=150, anchor=tk.CENTER)
        self.tree.column('author', width=130, minwidth=90, anchor=tk.CENTER)
        self.tree.column('category', width=178, minwidth=100, anchor=tk.W)
        self.tree.column('year', width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column('price', width=50, minwidth=50, stretch=tk.NO, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='Название')
        self.tree.heading('author', text='Автор')
        self.tree.heading('category', text='Раздел')
        self.tree.heading('year', text='Год')
        self.tree.heading('price', text='Цена')

        self.tree.pack()

        self.view_records()

    def records(self, name, author, category, year, price):
        self.lib.add_book(name, author, category, year, price)
        self.view_records()

    def update_record(self, name, author, category, year, price):
        index = self.tree.index(self.tree.selection()[0])
        book = self.lib.books[index]
        book.edit(book.ID, name, author, category, year, price)
        self.view_records()

    def view_records(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        for v in self.lib.books:
            self.tree.insert('', 'end', values=v.get())

    def open_add_dialog(self):
        AddBookWindow()

    def open_update_dialog(self):
        UpdateBookWindow()

class AddBookWindow(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_add()
        self.view = app

    def init_add(self):
        self.title("Добавить книгу")
        self.geometry("400x280+400+300")
        self.resizable(False, False)

        label_name = tk.Label(self, text="Название:")
        label_name.place(x=50, y=50)
        label_author = tk.Label(self, text="Автор:")
        label_author.place(x=50, y=80)
        label_category = tk.Label(self, text="Раздел:")
        label_category.place(x=50, y=110)
        label_year = tk.Label(self, text="Год издания:")
        label_year.place(x=50, y=140)
        label_price = tk.Label(self, text="Цена (руб.):")
        label_price.place(x=50, y=170)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_author = ttk.Entry(self)
        self.entry_author.place(x=200, y=80)
        self.entry_category = ttk.Entry(self)
        self.entry_category.place(x=200, y=110)
        self.entry_year = ttk.Entry(self)
        self.entry_year.place(x=200, y=140)
        self.entry_price = ttk.Entry(self)
        self.entry_price.place(x=200, y=170)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=230)

        btn_ok = ttk.Button(self, text="Добавить")
        btn_ok.place(x=220, y=230)
        btn_ok.bind('<Button-1>', self.click_OK)

        self.grab_set()
        self.focus_set()

    def click_OK(self, event):
        self.view.records(self.entry_name.get(),
                          self.entry_author.get(),
                          self.entry_category.get(),
                          self.entry_year.get(),
                          self.entry_price.get())
        self.destroy()

class UpdateBookWindow(AddBookWindow):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title("Редактировать данные")
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=220, y=230)
        btn_edit.bind('<Button-1>', self.click_edit)

    def click_edit(self, event):
        self.view.update_record(self.entry_name.get(),
                          self.entry_author.get(),
                          self.entry_category.get(),
                          self.entry_year.get(),
                          self.entry_price.get())
        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()

    lib = Library()
    lib.add_book("Анна Каренина", "Лев Толстой", "художественная литература", 1856, 345)
    lib.add_book("Укусь: мастерство гейш", "Гав Рыков", "учебная литература", 2018, 5)
    lib.add_book("Как кекать", "Сычуанский Ананас", "познавательная литература", 2020, 30000)
    lib.print_books()

    app = Main(root)
    app.pack()
    root.title("Библиотека")
    root.geometry("650x450+300+200")
    root.resizable(False, False)



    root.mainloop()