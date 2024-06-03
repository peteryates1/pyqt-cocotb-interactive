import sys
import os

from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from widgets.Switch import Switch
from widgets.SevenSegmentLED import SevenSegmentLED
from widgets.SwitchBank import SwitchBank

class NibbleSwitchDisplay(QWidget):
    value=pyqtSignal(int)

    @pyqtSlot(int)
    def update(self, value):
        self.ssdisp.update(value, False, True)
        self.value.emit(value)

    def createDisplay(self):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.addStretch(0)
        self.ssdisp = SevenSegmentLED()
        layout.addWidget(self.ssdisp)
        layout.addStretch(0)
        widget.setLayout(layout)
        return widget

    def __init__(self, numberOfSwitches:int=4):
        super(NibbleSwitchDisplay, self).__init__()
        layout = QVBoxLayout()
        layout.addWidget(self.createDisplay())
        self.switches = SwitchBank(width=numberOfSwitches)
        self.switches.value.connect(self.update)
        layout.addWidget(self.switches)
        self.setLayout(layout)
