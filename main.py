import tkinter as tk
from tkinter import ttk
from library import *
from book import *

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file='plus.gif')
        btn_open_add_dialog = tk.Button(toolbar, text='Добавить книгу', bg="#d7d8e0", bd=0,
                                        compound=tk.TOP, image=self.add_img)
        btn_open_add_dialog.pack(side=tk.LEFT)
        self.lib = lib

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

    def view_records(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        for v in self.lib.books:
            self.tree.insert('', 'end', values=v.get())


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