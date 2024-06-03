
from PyQt5.QtWidgets import QHBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal

from Switch import Switch

class SwitchBank(QWidget):
    value=pyqtSignal(int)

    def update(self):
        v = 0
        for i in range(len(self.switches)):
            v = (v << 1) | (1 if self.switches[i].value else 0)
        self.value.emit(v)

    def __init__(self, width:int=4):
        super(SwitchBank, self).__init__()
        layout = QHBoxLayout()
        layout.addStretch(0)
        self.switches = [Switch() for _ in range(width)]
        [layout.addWidget(switch) for switch in self.switches]
        [switch.clicked.connect(self.update) for switch in reversed(self.switches)]
        layout.addStretch(0)
        self.setLayout(layout)