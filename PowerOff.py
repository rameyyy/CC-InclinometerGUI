import os
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import sys

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Raspberry Pi Power Controler")
window.setGeometry(141, 80, 850, 60)
window.setFixedSize(850, 50)
window.setStyleSheet("background-color: lightgray;")

def btn_logout_clicked():
    os.system('pkill -u coopproject')

def btn_shutdown_logout_clicked():
    #os.system('pkill -u coopproject')
    os.system('sudo shutdown now')

def btn_reboot_clicked():
    os.system('sudo reboot')


btn_logout = QPushButton('Logout', window)
btn_logout.setGeometry(30, 8, 243, 35)
btn_logout.clicked.connect(btn_logout_clicked)
btn_shutdown_logout = QPushButton('Shutdown', window)
btn_shutdown_logout.setGeometry(303, 8, 244, 35)
btn_shutdown_logout.clicked.connect(btn_shutdown_logout_clicked)
btn_reboot = QPushButton('Reboot', window)
btn_reboot.setGeometry(577, 8, 243, 35)
btn_reboot.clicked.connect(btn_reboot_clicked)


window.show()

sys.exit(app.exec_())
# log out the current user
#os.system('pkill -u coopproject')
