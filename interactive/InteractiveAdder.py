import sys

import cocotb
from cocotb.triggers import Edge, NextTimeStep, Timer
from cocotb.handle import SimHandleBase
from cocotb.queue import Queue
from cocotb.binary import BinaryValue

from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QFont

sys.path.append('/home/peter/git/pyqt-cocotb-interactive/interactive/widgets')
from NibbleSwitchDisplay import NibbleSwitchDisplay
from SevenSegmentDisplay import SevenSegmentDisplay
from ConsumerMonitor import ConsumerMonitor
from ProducerMonitor import ProducerMonitor

def int_setter(h: SimHandleBase, v: int):
    h.value = v

class InteractiveAdder(QMainWindow):

    def withHeaderLabel(self, labelText : str, widgetToLabel : QWidget):
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        label = QLabel(labelText)
        label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(14)
        label.setFont(font)
        layout.addStretch()
        layout.addWidget(label)
        layout.addWidget(widgetToLabel)
        layout.addStretch()
        return widget

    def __init__(self, dut):
        super(InteractiveAdder, self).__init__()
        self.setWindowTitle('Interactive 4 Bit Full Adder')
        self.dut = dut
        dut.a.value = 0
        dut.b.value = 0
        dut.c.value = 0
        layout = QHBoxLayout()
        self.A = NibbleSwitchDisplay()
        layout.addWidget(self.withHeaderLabel("A", self.A))
        layout.addWidget(QLabel("+"))
        self.B = NibbleSwitchDisplay()
        layout.addWidget(self.withHeaderLabel("B", self.B))
        layout.addWidget(QLabel("+"))
        self.C = NibbleSwitchDisplay(numberOfSwitches=1)
        layout.addWidget(self.withHeaderLabel("C", self.C))
        layout.addWidget(QLabel("="))
        self.Q = SevenSegmentDisplay(numberOfDigits=2)
        layout.addWidget(self.withHeaderLabel("Q", self.Q))
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.run = True
        self.A_monitor = ConsumerMonitor[int, SimHandleBase](dut.a, int_setter)
        self.A.value.connect(lambda v: self.A_monitor.put_nowait(v))
        self.B_monitor = ConsumerMonitor[int, SimHandleBase](dut.b, int_setter)
        self.B.value.connect(lambda v: self.B_monitor.put_nowait(v))
        self.C_monitor = ConsumerMonitor[int, SimHandleBase](dut.c, int_setter)
        self.C.value.connect(lambda v: self.C_monitor.put_nowait(v))
        self.Q_monitor = ProducerMonitor[BinaryValue, SimHandleBase](dut.q, lambda h: h.value, lambda h: Edge(h))
        self.Q_monitor.value.connect(lambda value: self.q_update(value))
        self.A_monitor.start()
        self.B_monitor.start()
        self.C_monitor.start()
        self.Q_monitor.start()

    def q_update(self, value):
        if value.is_resolvable:
            self.Q.update(value.integer)
    
    def closeEvent(self, event):
        self.run = False
        event.accept()  # Accept the close event

@cocotb.test()
async def main(dut):
    app = QApplication(sys.argv)
    w = InteractiveAdder(dut)
    w.show()
    while(w.run):
        if(app.hasPendingEvents()):
            app.processEvents()
        await Timer(1, units="ns")
    cocotb.log.info('Done')

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    print("Run this simulation by calling make.")
    exit()
