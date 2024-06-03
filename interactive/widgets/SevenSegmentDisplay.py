from enum import Enum
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QMargins, QSize
from SevenSegmentLED import SevenSegmentLED

class SevenSegmentDisplay(QWidget):

    def __init__(self, numberOfDigits = 4):
        super(SevenSegmentDisplay, self).__init__()
        self.numberOfDigits = numberOfDigits
        self.setMinimumSize(self.numberOfDigits*36,55)
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.addStretch()
        self.setLayout(layout)
        self.ssled = [SevenSegmentLED() for _ in range(self.numberOfDigits)]
        [layout.addWidget(ssled) for ssled in reversed(self.ssled)]
        layout.addStretch()
        self.update(0)

    def update(self, value:int, dp:int=-1):
        values = [(value >> (i << 2)) & 0xF for i in range(self.numberOfDigits)]
        points = [dp==i for i in range(self.numberOfDigits)]
        on = [True if values[i] else False for i in range(self.numberOfDigits)]
        for i in range(self.numberOfDigits-2,-1,-1):
            on[i] = True if on[-1] else on[i]
        on[0] = True
        self.update_digits(values, points, on)

    def update_digits(self, values:[int], points:[bool], on:[bool]):
        for i,v in enumerate(values):
            self.ssled[i].update(values[i], points[i], on[i])
