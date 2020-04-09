import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from library import *
from book import *

class Main(tk.Frame):
    def __init__(self, root, lib, with_welcome_screen=False):
        super().__init__(root)
        self.lib = lib
        if with_welcome_screen:
            Welcome()
        self.init_main()

    def init_main(self):
        root.title("Новая библиотека")

        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open_add_dialog = tk.Button(toolbar, text='Добавить книгу',command=self.open_add_dialog,
                                        bg="#d7d8e0", bd=0, compound=tk.TOP)
        btn_open_add_dialog.pack(side=tk.LEFT)

        btn_open_update_dialog = tk.Button(toolbar, text='Редактировать данные', command=self.open_update_dialog,
                                        bg="#d7d8e0", bd=0, compound=tk.TOP)
        btn_open_update_dialog.pack(side=tk.LEFT)

        btn_delete = tk.Button(toolbar, text='Удалить книги', bg='#d7d8e0', bd=0,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        btn_save_library = tk.Button(toolbar, text='Сохранить', bg='#d7d8e0', bd=0,
                               compound=tk.TOP, command=self.save_library)
        btn_save_library.pack(side=tk.LEFT)

        btn_save_as_library = tk.Button(toolbar, text='Сохранить как', bg='#d7d8e0', bd=0,
                                     compound=tk.TOP, command=self.save_as_library)
        btn_save_as_library.pack(side=tk.LEFT)

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

        root.bind('<Control-s>', lambda event: self.save_library())

    def save_library(self):
        if self.lib.file == None:
            self.save_as_library()
            return
        data = self.lib.get_data()
        file_name = self.lib.file
        f = open(file_name, 'w')
        f.write(data)
        f.close()

        mb.showinfo("Сообщение", "Сохранение прошло успешно")

    def save_as_library(self):
        data = self.lib.get_data()
        file_name = fd.asksaveasfilename(filetypes=(("Library files", "*.lbf"),))
        if not file_name:
            return
        if not file_name.endswith(".lbf"):
            file_name += ".lbf"
        print(file_name)
        f = open(file_name, 'w')
        f.write(data)
        f.close()

        self.lib.file = file_name
        root.title(self.lib.file)
        mb.showinfo("Сообщение", "Сохранение прошло успешно")

    def records(self, name, author, category, year, price):
        self.lib.add_book(name, author, category, year, price)
        self.view_records()

    def update_record(self, name, author, category, year, price):
        index = self.tree.index(self.tree.selection()[0])
        book = self.lib.books[index]
        book.edit(book.ID, name, author, category, year, price)
        self.view_records()

    def delete_records(self):
        if len(self.tree.selection()) == 0:
            mb.showinfo("Сообщение", "Выберите книги для удаления")
            return
        if not mb.askokcancel("Подтверждение", "Удалить эти книги?"):
            return
        for selection_item in reversed(self.tree.selection()):
            index = self.tree.index(selection_item)
            del self.lib.books[index]
        self.view_records()



    def view_records(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        for v in self.lib.books:
            self.tree.insert('', 'end', values=v.get())

    def open_add_dialog(self):
        AddBookWindow()

    def open_update_dialog(self):
        if(not len(self.tree.selection()) == 1):
            mb.showinfo("Сообщение", "Необходимо выбрать одну книгу")
            return
        UpdateBookWindow()


class Welcome(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_welcome()

    def init_welcome(self):
        self.title("Библиотека")
        self.geometry("400x280+400+200")
        self.resizable(False, False)

        root.withdraw()

        btn_new_library = tk.Button(self, text='Новая библиотека', command=self.new_library,
                                        bg="#d7d8e0", bd=0, compound=tk.TOP)
        btn_new_library.pack(side=tk.LEFT)

        btn_open_library = tk.Button(self, text='Открыть библиотеку', command=self.open_library,
                                           bg="#d7d8e0", bd=0, compound=tk.TOP)
        btn_open_library.pack(side=tk.LEFT)

        self.wm_protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grab_set()
        self.focus_set()

    def new_library(self):
        root.deiconify()
        self.destroy()

    def open_library(self):
        print("Opening")
        root.deiconify()
        self.destroy()

    def on_closing(self):
        root.destroy()


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

        self.text_name = tk.StringVar()
        self.entry_name = ttk.Entry(self, textvariable=self.text_name)
        self.entry_name.place(x=200, y=50)
        self.text_author = tk.StringVar()
        self.entry_author = ttk.Entry(self, textvariable=self.text_author)
        self.entry_author.place(x=200, y=80)
        self.text_category = tk.StringVar()
        self.entry_category = ttk.Entry(self, textvariable=self.text_category)
        self.entry_category.place(x=200, y=110)
        self.text_year = tk.StringVar()
        self.entry_year = ttk.Entry(self, textvariable=self.text_year)
        self.entry_year.place(x=200, y=140)
        self.text_price = tk.StringVar()
        self.entry_price = ttk.Entry(self, textvariable=self.text_price)
        self.entry_price.place(x=200, y=170)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=230)

        btn_ok = ttk.Button(self, text="Добавить")
        btn_ok.place(x=220, y=230)
        btn_ok.bind('<Button-1>', self.click_OK)

        self.grab_set()
        self.focus_set()

    def is_correct_book(self):
        if(not self.entry_name.get()):
            mb.showinfo("Сообщение", "Введите название книги")
            return False
        if (not self.entry_author.get()):
            mb.showinfo("Сообщение", "Введите автора книги")
            return False
        if (not self.entry_category.get()):
            mb.showinfo("Сообщение", "Введите раздел книги")
            return False
        if (not self.entry_year.get().isdigit()):
            mb.showinfo("Сообщение", "Поле \"Год издания\" должно содержать число")
            return False
        if (not self.entry_price.get().isdigit()):
            mb.showinfo("Сообщение", "Поле \"Цена\" должно содержать число")
            return False

        return True

    def click_OK(self, event):
        if not self.is_correct_book():
            return
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

        index = self.view.tree.index(self.view.tree.selection()[0])
        book = self.view.lib.books[index]

        self.text_name.set(book.name)
        self.text_author.set(book.author)
        self.text_category.set(book.category)
        self.text_year.set(book.year)
        self.text_price.set(book.price)

        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=220, y=230)
        btn_edit.bind('<Button-1>', self.click_edit)

    def click_edit(self, event):
        if not self.is_correct_book():
            return

        self.view.update_record(self.entry_name.get(),
                          self.entry_author.get(),
                          self.entry_category.get(),
                          self.entry_year.get(),
                          self.entry_price.get())
        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()

    lid = Library()
    lid.add_book("Анна Каренина", "Лев Толстой", "художественная литература", 1856, 345)
    lid.add_book("Укусь: мастерство гейш", "Гав Рыков", "учебная литература", 2018, 5)
    lid.add_book("Как кекать", "Сычуанский Ананас", "познавательная литература", 2020, 30000)
    # lib.print_books()

    app = Main(root, lid, True)
    app.pack()
    root.geometry("650x450+300+200")
    root.resizable(False, False)


    root.mainloop()