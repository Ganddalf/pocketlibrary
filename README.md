# pocketlibrary
Учебный проект приложения-библиотеки. Позволяет сохранять данные о книгах, прикреплять их к таблицам, сортировать и прикреплять файлы на компьютере к книге в таблице, чтобы файл открывался по двойному клику.

![изображение](https://user-images.githubusercontent.com/61993625/138549460-6bd6a47d-7b60-44d7-a9e0-7cefb329169c.png)

# Запуск
Установить пакеты: qrcode и PIL (или pillow)
Windows : python main.py в папке проекта
Linux : python3 main.py в папке проекта

# Детали
Можно прикрепить к книге файл, который будет открываться при двойном клике по ней
В папке libraries можно потестить example_with_files.lbf. Файлы, которые можно прикрепить к этим книгам, лежат в папке book_files
Добавлено создание qr-кода для выбранной книги. По идее, надо бы по url, но пока по хешу книги
Сортировка всё так же работает по кликам на заголовках таблицы
Можно сохраняться Сtrl-S (в английской раскладке)
Множественный выбор через Ctrl (полезно только в случае удаления книг)
