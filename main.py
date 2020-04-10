import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from library import *
from book import *

class Main(tk.Frame):
    def __init__(self, root, lib):
        super().__init__(root)
        self.lib = lib
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

        btn_load_library = tk.Button(toolbar, text='Открыть', bg='#d7d8e0', bd=0,
                                        compound=tk.TOP, command=self.load_library)
        btn_load_library.pack(side=tk.LEFT)

        btn_new_library = tk.Button(toolbar, text='Создать', bg='#d7d8e0', bd=0,
                                     compound=tk.TOP, command=self.new_library)
        btn_new_library.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'author', 'category', 'year', 'price'),
                                 height=20, show="headings")
        self.tree.column('ID', width=50, minwidth=50, anchor=tk.CENTER)
        self.tree.column('name', width=350, minwidth=200, anchor=tk.CENTER)
        self.tree.column('author', width=212, minwidth=200, anchor=tk.CENTER)
        self.tree.column('category', width=245, minwidth=200, anchor=tk.W)
        self.tree.column('year', width=65, minwidth=60, anchor=tk.CENTER)
        self.tree.column('price', width=100, minwidth=80, stretch=tk.NO, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='Название')
        self.tree.heading('author', text='Автор')
        self.tree.heading('category', text='Раздел')
        self.tree.heading('year', text='Год')
        self.tree.heading('price', text='Цена')

        self.tree.pack()

        self.view_records()

        root.bind('<Control-s>', lambda event: self.save_library())
        root.wm_protocol("WM_DELETE_WINDOW", self.on_closing)

    def records(self, name, author, category, year, price):
        self.lib.add_book(name, author, category, year, price)
        self.view_records()

    def update_record(self, name, author, category, year, price):
        index = self.tree.index(self.tree.selection()[0])
        book = self.lib.books[index]
        book.edit(book.ID, name, author, category, year, price)
        self.view_records()
        self.lib.changed = True

    def delete_records(self):
        if len(self.tree.selection()) == 0:
            mb.showinfo("Сообщение", "Выберите книги для удаления")
            return
        if not mb.askokcancel("Подтверждение", "Удалить эти книги?"):
            return
        for selection_item in reversed(self.tree.selection()):
            index = self.tree.index(selection_item)
            del self.lib.books[index]
        self.lib.changed = True
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

    def new_library(self):
        if self.lib.changed:
            confirm = mb.askyesnocancel("Создать", "Сохранить текущую библиотеку?")
            if confirm:
                self.save_library()
            elif confirm is None:
                return

        self.lib.clear()
        root.title("Новая библиотека")
        self.view_records()

    def save_library(self):
        if self.lib.file == None:
            self.save_as_library()
            return
        data = self.lib.get_data()
        file_name = self.lib.file
        f = open(file_name, 'w', encoding='utf-8')
        f.write(data)
        f.close()
        self.lib.changed = False

        mb.showinfo("Сообщение", "Сохранение прошло успешно")

    def save_as_library(self):
        data = self.lib.get_data()

        file_name = fd.asksaveasfilename(filetypes=(("Library files", "*.lbf"),))
        if not file_name:
            return
        if not file_name.endswith(".lbf"):
            file_name += ".lbf"

        try:
            f = open(file_name, 'w', encoding='utf-8')
            f.write(data)
        except:
            mb.showerror("Ошибка", "Ошибка открытия или сохранения файла")
        finally:
             f.close()

        self.lib.file = file_name
        root.title(self.lib.file.split('\\')[-1].split('/')[-1])
        self.lib.changed = False

        mb.showinfo("Сообщение", "Сохранение прошло успешно")

    def load_library(self):
        if self.lib.changed:
            confirm = mb.askyesnocancel("Загрузка", "Сохранить текущую библиотеку?")
            if confirm:
                self.save_library()
            elif confirm is None:
                return

        file_name = fd.askopenfilename(filetypes=(("Library files", "*.lbf"),))
        if not file_name:
            return False
        try:
            f = open(file_name, encoding='utf-8')
            data = f.read()
        except:
            mb.showerror("Ошибка", "Ошибка открытия или чтения файла")
            return False
        finally:
            f.close()

        new_lib = Library()

        if not new_lib.set_data(data):
            del new_lib
            mb.showerror("Ошибка", "В файле неизвестные данные")
            return False

        prev_lib = self.lib
        self.lib = new_lib
        self.lib.file = file_name
        self.view_records()
        root.title(self.lib.file.split('\\')[-1].split('/')[-1])
        del prev_lib
        return True

    def on_closing(self):
        if self.lib.changed:
            confirm = mb.askyesnocancel("Выход", "Сохранить текущую библиотеку перед выходом?")
            if confirm:
                self.save_library()
                root.destroy()
            elif confirm is None:
                return
            else:
                root.destroy()
        else:
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

    app = Main(root, lid)
    app.pack()
    width = 1024
    height = 512
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    pos_x = (screen_width - width) // 2
    pos_y = (screen_height - height) // 2

    root.geometry('{}x{}+{}+{}'.format(width, height, pos_x, pos_y))
    root.resizable(False, False)

    root.mainloop()