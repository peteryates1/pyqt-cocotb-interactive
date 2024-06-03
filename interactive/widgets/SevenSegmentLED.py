import os
from enum import Enum
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel

class SevenSegmentLED(QLabel):
    class RADIX(Enum):
        HEX = 16
        BCD = 10
        def mapping(self,A,B,C,D,E,F,G,P):
            if(self is SevenSegmentLED.RADIX.HEX):
                return [
                    [A,B,C,D,E,F],   [B,C],         [A,B,D,E,G],   [A,B,C,D,G],
                    [B,C,F,G],       [A,C,D,F,G],   [A,C,D,E,F,G], [A,B,C],
                    [A,B,C,D,E,F,G], [A,B,C,D,F,G], [A,B,C,E,F,G], [C,D,E,F,G],
                    [A,D,E,F],       [B,C,D,E,G],   [A,D,E,F,G],   [A,E,F,G]
                ]
            elif self is SevenSegmentLED.RADIX.BCD:
                return [
                    [A,B,C,D,E,F],   [B,C],         [A,B,D,E,G],   [A,B,C,D,G],     [B,C,F,G],
                    [A,C,D,F,G],     [A,C,D,E,F,G], [A,B,C],       [A,B,C,D,E,F,G], [A,B,C,D,F,G],
                    [G],   # - for negative
                    [E,G]  # r for error
                ]
    
    OFF = None
    OFFP = None
    DIGIT = None
    DIGITP = None

    def init(radix:RADIX=RADIX.HEX):
        path = os.path.dirname(os.path.abspath(__file__))
        SevenSegmentLED.OFF = QPixmap(os.path.join(path, "images/7seg_base.png"))
        A = QPixmap(os.path.join(path, "images/7seg_a.png"))
        B = QPixmap(os.path.join(path, "images/7seg_b.png"))
        C = QPixmap(os.path.join(path, "images/7seg_c.png"))
        D = QPixmap(os.path.join(path, "images/7seg_d.png"))
        E = QPixmap(os.path.join(path, "images/7seg_e.png"))
        F = QPixmap(os.path.join(path, "images/7seg_f.png"))
        G = QPixmap(os.path.join(path, "images/7seg_g.png"))
        P = QPixmap(os.path.join(path, "images/7seg_p.png"))
        mapping = radix.mapping(A,B,C,D,E,F,G,P)
        SevenSegmentLED.DIGIT=[]
        SevenSegmentLED.DIGITP=[]
        for i in range(len(mapping)):
            digit = QPixmap(SevenSegmentLED.OFF)
            painter = QPainter(digit)
            for p in mapping[i]:
                painter.drawPixmap(QtCore.QPoint(), p)
            SevenSegmentLED.DIGIT.append(QPixmap(digit))
            painter.drawPixmap(QtCore.QPoint(), P)
            SevenSegmentLED.DIGITP.append(digit)
            painter.end()
        digitp = QPixmap(SevenSegmentLED.OFF)
        painter = QPainter(digitp)
        painter.drawPixmap(QtCore.QPoint(), P)
        painter.end()
        SevenSegmentLED.OFFP = digitp

    def __init__(self, *args, **kwargs):
        super(QLabel, self).__init__()
        if not SevenSegmentLED.OFF: SevenSegmentLED.init()#radix=kwargs.get('radix', RADIX.BCD))
        self.setPixmap(QPixmap(SevenSegmentLED.DIGIT[0]))
        self.setMinimumSize(35,50)

    def sizeHint(self):
        return QtCore.QSize(35,50)

    def update(self, value, point, on):
        if on:
            self.setPixmap(SevenSegmentLED.DIGITP[value] if point else SevenSegmentLED.DIGIT[value])
        else:
            self.setPixmap(SevenSegmentLED.OFFP if point else SevenSegmentLED.OFF)
