import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow
)

from PyQt5.uic import loadUi

from main_window_ui import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        #self.connectSignalsSlots(self)

    #def connectSignalsSlots(self):
        #self.action_Exit.triggered.connect(self.close)
        #self.action_Find_Replace.triggered.connect(self.findAndReplace)
        #self.action_About.triggered.connect(self.about)

    def setParameters(self):
        print("Parameters set!")
        self.statusLabel.setText("Parameters set!")

    def refresh(self):
        print("Refreshed!")
        self.statusLabel.setText("Parameters refreshed.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    temp = 25   # temperature variable is initiated to a default value.
    hum = 10    # humidity variable is initiated to a default value.
    win.show()
    sys.exit(app.exec())
