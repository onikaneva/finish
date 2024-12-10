import sqlite3
import sys

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QPushButton

from book_info_ui import Ui_Form as Ui_Book
from main_ui import Ui_Form


class MainWidget(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        # uic.loadUi("./static/ui/main.ui", self)
        self.setupUi(self)
        self.con = sqlite3.connect("./db/library.db")
        self.params = {"Автор": "author", "Название": "title"}
        self.searchButton.clicked.connect(self.search)

    def search(self):
        self.listWidget.clear()
        el = self.comboBox.currentText()
        if self.params.get(el) == "title":
            req = "SELECT id,title FROM books WHERE title LIKE '%{}%'".format(self.Title.text())
        else:
            req = "SELECT id,title FROM books WHERE author in (SELECT id from authors WHERE surname LIKE '%{}%')".format(
                self.Title.text())
        cur = self.con.cursor()
        data = cur.execute(req).fetchall()
        elems = [[QPushButton(i[1], self), i[0]] for i in data]
        for btn, loc_id in elems:
            btn.clicked.connect(self.show_info(loc_id))

        items = [QListWidgetItem() for _ in elems]
        for i in range(len(items)):
            self.listWidget.addItem(items[i])
            items[i].setSizeHint(elems[i][0].sizeHint())
            self.listWidget.setItemWidget(items[i], elems[i][0])

    def show_info(self, loc_id):
        def call_info():
            cur = self.con.cursor()
            title, year, author_id, image, genre_id = cur.execute(
                f"SELECT title,year,author,image,genre From books Where id = {loc_id}").fetchone()
            author = " ".join(cur.execute(f"SELECT surname,name from authors where id={author_id}").fetchone())
            genre = cur.execute(f"SELECT title FROM genres WHERE id ={genre_id}").fetchone()[0]
            if image:
                info_book = BookWidget(self, title, author, str(year), genre, './static/img/' + image)
            else:
                info_book = BookWidget(self, title, author, str(year), genre)
            info_book.show()

        return call_info


class BookWidget(QMainWindow, Ui_Book):
    def __init__(self, parent=None, title=None, author=None, year=None, genre=None, image='./static/img/noname.png'):
        super().__init__(parent)
        # uic.loadUi("./static/ui/book_info.ui", self)
        self.setupUi(self)
        self.label_3.setText(title)
        self.label_7.setText(author)
        self.label_4.setText(year)
        self.label_8.setText(genre)

        self.pixmap = QPixmap(image)
        self.label.setPixmap(self.pixmap)


app = QApplication(sys.argv)
ex = MainWidget()
ex.show()
sys.exit(app.exec())
