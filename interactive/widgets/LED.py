import os
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel

class LED(QLabel):
    
    OFF = None
    ON = None

    def init():
        path = os.path.dirname(os.path.abspath(__file__))
        LED.OFF = QPixmap(os.path.join(path, "images/led_off.png"))
        LED.ON = QPixmap(os.path.join(path, "images/led_on.png"))

    def __init__(self):
        super(QLabel, self).__init__()
        if not LED.OFF: LED.init()
        self.setPixmap(LED.OFF)

    def sizeHint(self):
        return QtCore.QSize(25,25)

    def update(self, value):
        if not value:
            self.setPixmap(LED.OFF)
        else:
            self.setPixmap(LED.ON)
