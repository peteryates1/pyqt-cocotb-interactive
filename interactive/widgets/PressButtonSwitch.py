import os

from PyQt5.QtCore import pyqtSignal, QPoint, QSize
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QLabel

class PressButtonSwitch(QLabel):
    change=pyqtSignal(int)
    pixmap = None

    def init():
        path = os.path.dirname(os.path.abspath(__file__))
        HOR = [QPixmap(os.path.join(path, "images/button_pads_h.png")), QPixmap(os.path.join(path, "images/button_pads_v.png"))]
        VAL = [QPixmap(os.path.join(path, "images/button.png")), QPixmap(os.path.join(path, "images/button_pressed.png"))]
        SEL = [QPixmap(os.path.join(path, "images/button_s.png")), QPixmap(os.path.join(path, "images/button_pressed_s.png"))]
        PressButtonSwitch.pixmap = []
        for hor in range(2):
            PressButtonSwitch.pixmap.append([])
            for val in range(2):
                PressButtonSwitch.pixmap[hor].append([])
                pixmap = QPixmap(HOR[hor])
                painter = QPainter(pixmap)
                painter.drawPixmap(QPoint(), VAL[val])
                painter.end()
                PressButtonSwitch.pixmap[hor][val].append(pixmap)
                pixmap = QPixmap(HOR[hor])
                painter = QPainter(pixmap)
                painter.drawPixmap(QPoint(), SEL[val])
                painter.end()
                PressButtonSwitch.pixmap[hor][val].append(pixmap)
    
    def __init__(self, horizontal = True):
        super(QLabel, self).__init__()
        if not PressButtonSwitch.pixmap: PressButtonSwitch.init()
        self.value = 0
        self.horizontal = 0 if horizontal else 1
        self.mouseInWidget = 0
        self.setMouseTracking(True)
        self.update()

    def sizeHint(self):
        return QSize(30,55)
    
    def update(self):
        self.setPixmap(PressButtonSwitch.pixmap[self.horizontal][self.value][self.mouseInWidget])
    
    def mousePressEvent(self, e):
        self.value = 1
        self.update()
        self.change.emit(self.value)

    def mouseReleaseEvent(self, e):
        self.value = 0
        self.update()
        self.change.emit(self.value)
        
    def leaveEvent(self,e):
        self.mouseInWidget = 0
        self.update()

    def enterEvent(self,e):
        self.mouseInWidget = 1
        self.update()
