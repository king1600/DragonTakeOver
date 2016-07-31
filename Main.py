import sys
import os

from PySide.QtGui import QWidget, QApplication
from widgets import *
from Game import Game

PLAYER    = None

class MainWindow(QWidget):
    WIDTH  = 640
    HEIGHT = 480

    is_ready  = False
    CHARACTER = "Crystal"
    NEW_GAME  = False

    def __init__(self):
        super(MainWindow, self).__init__()
        self.game = Game()
        self.game.music = self.game.rsc.load_song('blade_of_hope')
        self.game.music.set_volume(self.game.bg_vol)
        self.game.music.play(-1)

        self.initUI()
        self.create_widgets()
        self.layout.addStretch(1)

        self.draw_bg()

    def initUI(self):
        self.resize(self.WIDTH, self.HEIGHT)
        self.setFixedSize(QSize(self.WIDTH+20, self.HEIGHT+90))
        self.setWindowTitle("Dragon TakeOver")

        ico_path = os.path.join("resources","images","icon.png")
        self.setWindowIcon(QIcon(ico_path))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def create_widgets(self):
        self.logo = ImageLabel("","resources/images/logo.png")
        self.logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo)

        self.cs = ChoiceScreen(self)
        self.layout.addWidget(self.cs)

    def draw_bg(self):
        path = os.path.join("resources", "images", "flame_bg.jpg")
        pixmap = QPixmap(path).scaled(self.WIDTH*5, self.HEIGHT*5)
        pallete = QPalette()
        pallete.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(pallete)

def load_game(win):
    win.game.init(win.CHARACTER)
    if win.NEW_GAME:
        #win.game.scences.load_scence(1)
        win.game.manager.load_level("village")
    win.game.run()

class temp:
    def __init__(self):
        self.game = Game()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()

    if win.is_ready:
        load_game(win)

    sys.exit()