import os
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel

class Switch(QLabel):
    clicked=pyqtSignal(bool)

    OFF = None
    ON = None
    OFFS = None
    ONS = None

    def init():
        path = os.path.dirname(os.path.abspath(__file__))
        Switch.OFF = QPixmap(os.path.join(path, "images/switch_off.png"))
        Switch.ON = QPixmap(os.path.join(path, "images/switch_on.png"))
        Switch.OFFS = QPixmap(os.path.join(path, "images/switch_off_s.png"))
        Switch.ONS = QPixmap(os.path.join(path, "images/switch_on_s.png"))
    
    def __init__(self):
        super(QLabel, self).__init__()
        if not Switch.OFF: Switch.init()
        self.setPixmap(Switch.OFF)
        self.value = False
        self.mouseInWidget = False
        self.setMouseTracking(True)

    def sizeHint(self):
        return QtCore.QSize(30,55)
    
    def update(self):
        if not self.value:
            self.setPixmap(Switch.OFFS if self.mouseInWidget else Switch.OFF)
        else:
            self.setPixmap(Switch.ONS if self.mouseInWidget else Switch.ON)
    
    def mousePressEvent(self, e):
        self.value = not self.value
        self.update()
        self.clicked.emit(self.value)

    def leaveEvent(self,e):
        self.mouseInWidget = False
        self.update()

    def enterEvent(self,e):
        self.mouseInWidget = True
        self.update()
    