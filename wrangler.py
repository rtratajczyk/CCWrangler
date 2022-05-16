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

        #self.connect(s)
        #self.connectSignalsSlots(self)

    temp = 25   # temperature and humidity variables are initiated to their default values.
    hum = 10
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    connected = False

    #def connectSignalsSlots(self):
        #self.action_Exit.triggered.connect(self.close)
        #self.action_Find_Replace.triggered.connect(self.findAndReplace)
        #self.action_About.triggered.connect(self.about)

    def connToCC(self):
        print("Trying to connect...")
        if(self.connected == False):
            self.sock.close()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(1)
        self.statusLabel.setText("Now attempting to connect to the Climatic Chamber...")
        try:
            print('Trying to connect to ' + self.ipLineEdit.text())
            self.sock.connect((self.ipLineEdit.text(), 2049))  # Attempting to connect to the socket to the climatic chamber. Address grabbed from input.
        except socket.timeout:
            print("oops cant connect huh")

            self.statusLabel.setText("Cannot connect to the climatic chamber. Is it on and is the address correct?")
            #time.sleep(3)  # To give user time to read the error message.
            #quit()
        """if self.sock.getpeername() == (self.ipLineEdit.text(), 2049):  # Double check if we are definitely connected to the chamber.
            self.statusLabel.setText("Successfully connected with the climatic chamber!")
        else:
            self.statusLabel.setText("Connected to something, but the IP address is not what was expected."
                                     " Please investigate this problem and retry.")
            #time.sleep(10)  # To give user time to read the error message.
            #quit()"""


    def setParameters(self):
        self.tempLineFix()
        self.humLineFix()

        self.temp = int(self.tempLineEdit.text())
        self.hum = int(self.humLineEdit.text())
        print("Now setting the temperature to " + str(self.temp) + " and humidity to " + str(self.hum))
        message = "$01E " + str(self.temp) + " " + str(self.hum) + " 100 1200 010000000000000000000 \r"
        self.sock.sendall(message.encode("ascii"))

        self.statusLabel.setText("Parameters sent to chamber! Current target"
                                 " temperature: " + str(self.temp) + " degrees Celsius; current target humidity: " + str(self.hum) + "%. Please stand by.")
        self.lcdTemp.display(self.temp)
        self.lcdHum.display(self.hum)

    def refresh(self):
        message = "$01I \r"  # This string asks the chamber for its current values.
        self.sock.sendall(message.encode("ascii"))
        response = self.sock.recv(4096).decode()
        # print("Response: " + str(response))

        split_response = response.split(" ")
        self.temp = split_response[1]
        self.hum = split_response[2]
        self.lcdTemp.display(self.temp)
        self.lcdHum.display(self.hum)
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
