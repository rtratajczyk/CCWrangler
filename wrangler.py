import sys
import time
import socket

from PyQt5.QtWidgets import (
    QApplication, QMainWindow
)

from PyQt5.uic import loadUi

from main_window_new_ui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.settimeout(5)
        #self.connect(s)
        #self.connectSignalsSlots(self)

    temp = 25   # temperature and humidity variables are initiated to their default values.
    hum = 10


    #def connectSignalsSlots(self):
        #self.action_Exit.triggered.connect(self.close)
        #self.action_Find_Replace.triggered.connect(self.findAndReplace)
        #self.action_About.triggered.connect(self.about)

    def connect(self, sock):
        self.statusLabel.setText("Now attempting to connect to the Climatic Chamber...")
        try:
            sock.connect(('10.10.21.238',
                       2049))  # Attempting to connect to the socket to the climatic chamber. Address hardcoded.
        except socket.timeout:
            self.statusLabel.setText("Cannot connect to the climatic chamber. Please make sure that it is turned on, "
                  " connected to the network, set to external control and then run the script again.")
            #time.sleep(10)  # To give user time to read the error message.
            #quit()
        if sock.getpeername() == ('10.10.21.238', 2049):  # Double check if we are definitely connected to the chamber.
            self.statusLabel.setText("Successfully connected with the climatic chamber!")
        else:
            self.statusLabel.setText("Connected to something, but the IP address is not what was expected."
                                     " Please investigate this problem and retry.")
            #time.sleep(10)  # To give user time to read the error message.
            #quit()


    def setParameters(self):
        self.tempLineFix()
        self.humLineFix()

        self.temp = int(self.tempLineEdit.text())
        self.hum = int(self.humLineEdit.text())
        self.statusLabel.setText("Parameters sent to chamber! Current target"
                                 " temperature: " + str(self.temp) + " degrees Celsius; current target humidity: " + str(self.hum) + "%. Please stand by.")
        self.lcdTemp.display(self.temp)
        self.lcdHum.display(self.hum)

    def refresh(self):
        print("Refreshed!")
        self.statusLabel.setText("Parameters refreshed.")

    def humChange(self):
        self.hum = self.humDial.value()
        self.humLineEdit.setText(str(self.hum))

    def tempChange(self):
        self.temp = self.tempDial.value()
        self.tempLineEdit.setText(str(self.temp))

    def humLineFix(self):
        if int(self.humLineEdit.text()) > 98:
            self.humLineEdit.setText("98")
            return 1
        elif int(self.humLineEdit.text()) < 10:
            self.humLineEdit.setText("10")
            return 2

    def tempLineFix(self):
        if int(self.tempLineEdit.text()) > 190:
            self.tempLineEdit.setText("190")
            return 1
        elif int(self.tempLineEdit.text()) < -40:
            self.tempLineEdit.setText("-40")
            return 2




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
