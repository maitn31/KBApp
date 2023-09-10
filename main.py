import PyQt5.uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5 import QtWidgets
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        PyQt5.uic.loadUi("kbapp.ui", self)
        self.setWindowTitle("KB Table Timer")
        self.timer_labels = []
        self.table_labels = []
        self.checkin_buttons = []
        self.checkout_buttons = []

        timer = QTimer(self)
        timer.timeout.connect(self.update_timer)
        timer.start(1000)

        for i in range(1, 19):
            table_label_name = f"table_{i}"
            table_label = self.findChild(QLabel, table_label_name)
            if table_label:
                self.table_labels.append(table_label)

            timer_label_name = f"timer_{i}"
            timer_label = self.findChild(QLabel, timer_label_name)

            if timer_label:
                self.timer_labels.append(timer_label)

            checkin_button_name = f"checkin_{i}"
            checkin_button = self.findChild(QPushButton, checkin_button_name)

            checkout_button_name = f"checkout_{i}"
            checkout_button = self.findChild(QPushButton, checkout_button_name)

            if checkin_button:
                checkin_button.clicked.connect(lambda _, m=i: self.check_in(m - 1))
                self.checkin_buttons.append(checkin_button)
            if checkout_button:
                checkout_button.clicked.connect(lambda _, n=i: self.check_out(n - 1))
                self.checkout_buttons.append(checkout_button)

        # self.is_checked_in = [False] * 18
        self.show()

    def check_in(self, index):
        # if not self.is_checked_in[index]:
        # Get the current time and add 2 hours
        if self.timer_labels[index].text() != "Time":
            values = QtWidgets.QInputDialog.getText(
                QDialog(), 'Edit Timer', 'Enter new time:')
            print(values)
            new_time = QTime()
            try:
                parts = values[0].split(':')
                formatted_parts = [f'{int(part):02}' for part in parts]
                formatted_time_str = ':'.join(formatted_parts)
                new_time = QTime.fromString(formatted_time_str, "hh:mm:ss")
            except ValueError:
                print("Tieme is not valid")
            if new_time.isValid():
                self.timer_labels[index].setText(new_time.toString("hh:mm:ss"))


        else:
            current_time = QTime.currentTime()
            future_time = current_time.addSecs(2 * 60 * 60)  # 2 hours in seconds
            self.timer_labels[index].setText(future_time.toString("hh:mm:ss"))
            # self.is_checked_in[index] = True
            self.table_labels[index].setStyleSheet("background-color: green;")

    def check_out(self, index):
        self.timer_labels[index].setText("Time")
        self.table_labels[index].setStyleSheet("")

    def update_timer(self):
        for i in range(18):
            if self.timer_labels[i].text() != "Time":
                current_time = QTime.currentTime()
                detected_time = QTime.fromString(self.timer_labels[i].text(), "hh:mm:ss")
                if detected_time < current_time:
                    self.table_labels[i].setStyleSheet("background-color: red;")


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())
