# coding: utf8
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from library import Library


class Main(tk.Frame):
    def __init__(self, root, lib):
        super().__init__(root)
        self.lib = lib
        self.init_main()

    def init_main(self):
        try:
            root.iconbitmap('icons/books.ico')
        except:
            print('Can\'t load icon')
        root.title("Новая библиотека")

        toolbar = tk.Frame(bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        image_files = ['icons/add_folder.gif', 'icons/folder.gif',
                       'icons/save.gif', 'icons/add_book.gif',
                       'icons/edit_book.gif', 'icons/remove_book.gif']
        self.images = list(map(lambda x: tk.PhotoImage(file=x), image_files))

        buttons_data = [['Создать', self.new_library, self.images[0]],
                           ['Открыть', self.load_library, self.images[1]],
                           ['Сохранить', self.save_library, self.images[2]],
                           ['Сохранить как', self.save_as_library, self.images[2]],
                           ['Добавить книгу', self.open_add_dialog, self.images[3]],
                           ['Редактировать', self.open_update_dialog, self.images[4]],
                           ['Удалить книги', self.delete_records, self.images[5]]]

        def new_button(btn):
            return tk.Button(toolbar, text=btn[0], bd=0, width=100,
                             compound=tk.TOP, command=btn[1], image=btn[2])

        self.buttons = list(map(new_button, buttons_data))
        for button in self.buttons:
            button.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'author',
                                                'category', 'year', 'price'),
                                 height=20, show="headings")
        columns_data = [['ID', 'ID', 50, 50, tk.CENTER],
                        ['name', 'Название', 350, 200, tk.CENTER],
                        ['author', 'Автор', 212, 200, tk.CENTER],
                        ['category', 'Раздел', 245, 200, tk.CENTER],
                        ['year', 'Год', 65, 60, tk.CENTER],
                        ['price', 'Цена', 100, 80, tk.CENTER]]

        def set_column(data):
            self.tree.column(data[0], width=data[2], minwidth=data[3],
                             anchor=data[4])
            self.tree.heading(data[0], text=data[1],
                              command=lambda: self.click_on_heading(data[0]))

        list(map(set_column, columns_data))
        self.tree.column('price', stretch=tk.NO)

        self.tree.pack()

        self.view_records()

        root.bind('<Control-s>', lambda event: self.save_library())
        root.wm_protocol("WM_DELETE_WINDOW", self.on_closing)

    def click_on_heading(self, str):
        self.lib.sort_by_attribute(str)
        self.view_records()

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

    @staticmethod
    def open_add_dialog():
        AddBookWindow()

    def open_update_dialog(self):
        if not len(self.tree.selection()) == 1:
            mb.showinfo("Сообщение", "Необходимо выбрать одну книгу")
            return
        UpdateBookWindow()

    def new_library(self):
        if self.lib.changed:
            confirm = mb.askyesnocancel("Создать",
                                        "Сохранить текущую библиотеку?")
            if confirm:
                self.save_library()
            elif confirm is None:
                return

        self.lib.clear()
        root.title("Новая библиотека")
        self.view_records()

    def save_library(self):
        if self.lib.file is None:
            self.save_as_library()
            return
        data = self.lib.get_data()
        file_name = self.lib.file

        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(data)
        except:
            mb.showerror("Ошибка", "Ошибка открытия или сохранения файла")

        self.lib.changed = False

        mb.showinfo("Сообщение", "Сохранение прошло успешно")

    def save_as_library(self):
        data = self.lib.get_data()

        file_name = fd.asksaveasfilename(filetypes=(("Library files",
                                                     "*.lbf"),))
        if not file_name:
            return
        if not file_name.endswith(".lbf"):
            file_name += ".lbf"

        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(data)
        except:
            mb.showerror("Ошибка", "Ошибка открытия или сохранения файла")

        self.lib.file = file_name
        root.title(self.lib.file.split('\\')[-1].split('/')[-1])
        self.lib.changed = False

        mb.showinfo("Сообщение", "Сохранение прошло успешно")

    def load_library(self):
        if self.lib.changed:
            confirm = mb.askyesnocancel("Загрузка",
                                        "Сохранить текущую библиотеку?")
            if confirm:
                self.save_library()
            elif confirm is None:
                return

        file_name = fd.askopenfilename(filetypes=(("Library files", "*.lbf"),))
        if not file_name:
            return False
        try:
            with open(file_name, encoding='utf-8') as f:
                data = f.read()
        except:
            mb.showerror("Ошибка", "Ошибка открытия или чтения файла")
            return False

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
            confirm = mb.askyesnocancel("Выход", "Сохранить текущую"
                                        " библиотеку перед выходом?")
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
        try:
            self.iconbitmap("icons/book.ico")
        except:
            print('Can\'t load icon')

    def init_add(self):
        self.title("Добавить книгу")
        self.geometry("450x280+400+300")
        self.resizable(False, False)

        fields_data = [["Название:", 50, 0],
                       ["Автор:", 80, 1],
                       ["Раздел:", 110, 2],
                       ["Год издания:", 140, 3],
                       ["Цена (руб.)", 170, 4]]

        def set_label(data):
            tmp_label = tk.Label(self, text=data[0])
            tmp_label.place(x=50, y=data[1])

        list(map(set_label, fields_data))

        self.text_vars = [tk.StringVar() for x in range(len(fields_data))]

        def set_entry(data):
            tmp_entry = ttk.Entry(self, textvariable=self.text_vars[data[2]],
                                  width=30)
            tmp_entry.place(x=160, y=data[1])
            return tmp_entry

        self.entries = list(map(set_entry, fields_data))

        self.add_buttons()

        self.grab_set()
        self.lift(root)
        self.focus_set()

    def add_buttons(self):
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=30, y=230)

        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=320, y=230)
        self.btn_ok.bind('<Button-1>', self.click_ok)

    def is_correct_book(self):

        if not self.entries[0].get():
            mb.showinfo("Сообщение", "Введите название книги")
            return False
        if not self.entries[1].get():
            mb.showinfo("Сообщение", "Введите автора книги")
            return False
        if not self.entries[2].get():
            mb.showinfo("Сообщение", "Введите раздел книги")
            return False
        if not self.entries[3].get().isdigit():
            mb.showinfo("Сообщение",
                        "Поле \"Год издания\" должно содержать число")
            return False
        if not self.entries[4].get().isdigit():
            mb.showinfo("Сообщение", "Поле \"Цена\" должно содержать число")
            return False

        return True

    def click_ok(self, event):
        if not self.is_correct_book():
            self.lift(root)
            return

        self.view.lib.changed = True

        self.view.records(*[x.get() for x in self.entries])
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

        self.text_vars[0].set(book.name)
        self.text_vars[1].set(book.author)
        self.text_vars[2].set(book.category)
        self.text_vars[3].set(book.year)
        self.text_vars[4].set(book.price)

    def add_buttons(self):
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=300, y=230)
        btn_edit.bind('<Button-1>', self.click_edit)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=30, y=230)

    def click_edit(self, event):
        if not self.is_correct_book():
            self.lift(root)
            return

        self.view.lib.changed = True

        self.view.update_record(*[x.get() for x in self.entries])
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
