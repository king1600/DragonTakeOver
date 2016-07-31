from PySide.QtGui import *
from PySide.QtCore import *
import os

class ChoiceScreen(QFrame):
    WIDTH  = 640
    HEIGHT = 480
    SAVE_FILE = "save.json"
    CHARACTER = None

    def __init__(self, parent=None):
        super(ChoiceScreen, self).__init__()
        self.win = parent
        self.WIDTH, self.HEIGHT = parent.WIDTH, parent.HEIGHT
        self.initUI()

    def initUI(self):
        self.resize(self.WIDTH, self.HEIGHT)
        self.setMinimumWidth(self.WIDTH)
        self.setMinimumHeight(self.HEIGHT)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.draw_bg()
        self.create_widgets()

    def create_widgets(self):
        self.box_path = os.path.join("resources","images","gold_box.png")

        self.frame_1 = QFrame()
        self.frame_1.layout = QGridLayout()
        self.frame_1.setLayout(self.frame_1.layout)

        self.frame_2 = QFrame()
        self.frame_2.layout = QGridLayout()
        self.frame_2.setLayout(self.frame_2.layout)

        self.frame_2.hide()
        self.frame_1.show()

        self.layout.addWidget(self.frame_1)
        self.layout.addWidget(self.frame_2)

        self.create_frame_2()

        self.new_game  = CustomButton("New Game", self.box_path, (270, 90))
        self.new_game.setAlignment(Qt.AlignCenter)
        self.new_game.clicked.connect(self.delete_save)
        self.frame_1.layout.addWidget(self.new_game, 0, 0)

        if os.path.exists(self.SAVE_FILE):
            self.load_game = CustomButton("Load Game", self.box_path, (270, 90))
            self.load_game.setAlignment(Qt.AlignCenter)
            self.load_game.clicked.connect(self.start_game)
            self.frame_1.layout.addWidget(self.load_game, 1, 0)

    def create_frame_2(self):
        self.mage = Character("crystal")
        self.knight = Character("jack")
        self.being = Character("nathan")

        self.chars = {
            "crystal": self.mage,
            "jack": self.knight,
            "nathan": self.being
        }
        for x in self.chars:
            self.chars[x].clicked.connect(self.set_character)
        self.set_character("crystal")

        title = QLabel("Pick a character")
        title.setStyleSheet("font-size:42px;")
        title.setAlignment(Qt.AlignCenter)

        img_layout = QHBoxLayout()
        img_layout.addWidget(self.mage)
        img_layout.addWidget(self.knight)
        img_layout.addWidget(self.being)

        self.go_button = CustomButton("Start Game",self.box_path, (490, 120))
        self.go_button.setAlignment(Qt.AlignCenter)
        self.go_button.clicked.connect(self.start_game)

        self.frame_2.layout.addWidget(title)
        self.frame_2.layout.addLayout(img_layout, 1, 0)
        self.frame_2.layout.addWidget(self.go_button, 2, 0)

    def set_character(self, name):
        self.win.game.name = name
        self.win.CHARACTER = name
        for x in self.chars:
            if name == x:
                self.chars[x].setStyleSheet("background-color: red;")
            else:
                self.chars[x].setStyleSheet("background-color: blue;")

    def draw_bg(self):
        path = os.path.join("resources", "images", "box.png")
        self.setAutoFillBackground(True)
        pixmap = QPixmap(path).scaled(self.WIDTH, self.HEIGHT)
        pallete = QPalette()
        pallete.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(pallete)

    def delete_save(self):
        if os.path.exists(self.SAVE_FILE):
            os.remove(self.SAVE_FILE)

        self.win.NEW_GAME = True
        self.frame_1.hide()
        self.frame_2.show()
        #self.start_game()

    def start_game(self):
        self.win.is_ready = True
        self.win.close()
        QCoreApplication.instance().quit()

class Character(QLabel):
    clicked = Signal(str)

    def __init__(self, name=''):
        self.name = name
        path = os.path.join("resources","images",name.lower()+".png")
        self._img = QImage(os.path.abspath(path))
        self.p_img = QPixmap.fromImage(self._img)
        self.p_img = self.p_img.scaled(140, 180)
        size = 160, 200

        super(Character, self).__init__()
        self.setMinimumSize(QSize(size[0], size[1]))
        self.setMaximumSize(QSize(size[0], size[1]))
        self.setStyleSheet("background-color: blue;")

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(10, 10, self.p_img)
        painter.end()

    def mousePressEvent(self, event):
        self.clicked.emit(self.name)

class ImageLabel(QLabel):
    clicked = Signal()

    def __init__(self, text='', path=None, _size=None):
        QLabel.__init__(self,text)
        self._size = _size
        self.setImage(path)

    def setImage(self, path):
        if '/' in path:
            temp = path.split('/')
            path = os.path.join(*temp)

        size = self._size
        if size is not None:
            self.pixmap = QPixmap(path).scaled(size[0],size[1], Qt.KeepAspectRatio)
        else:
            self.pixmap = QPixmap(path)
        self.setPixmap(self.pixmap)

    def mousePressEvent(self, event):
        self.clicked.emit()

class CustomButton(QLabel):
    clicked = Signal()

    def __init__(self, text='', path=None, size=None):
        path = os.path.abspath(path)
        self._size = size
        self._img = QImage(path)
        self._img = QPixmap().fromImage(self._img)
        self._img = self._img.scaled(self._size[0], self._size[1])
        self._text = text

        super(CustomButton, self).__init__()

        if size is not None:
            self.setMaximumSize(QSize(size[0],size[1]))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: blue;")

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.drawPixmap(0, 0, self._img)

        painter.setPen(QColor(10, 10, 10))
        painter.setFont(QFont("Decorative", 20))
        painter.drawText(event.rect(), Qt.AlignCenter, self._text)

        painter.end()

    def mousePressEvent(self, event):
        self.clicked.emit()
