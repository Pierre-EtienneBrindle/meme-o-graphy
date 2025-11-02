from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QTextEdit, QCheckBox, QLabel, QComboBox

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("meme-o-graphy")

        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)

        self.textbox = QTextEdit()
        self.sign_checkbox = QCheckBox()
        self.sign_label = QLabel("Sign message")
        self.encrypt_for_me_checkbox = QCheckBox()
        self.encrypt_for_me_label = QLabel("Encrypt for me")
        self.recipients_label = QLabel("Select recipients")
        self.recipients_list = QComboBox()
        self.recipients_list.addItems(["test", "yo", "men", "Alexandre Blais"])
        self.select_recipient = QPushButton("Add")

        self.layout.addWidget(self.textbox, 0, 0, 5, 5)
        self.layout.addWidget(self.sign_checkbox, 0, 5, 1, 1)
        self.layout.addWidget(self.sign_label, 0, 6, 1, 3)
        self.layout.addWidget(self.encrypt_for_me_checkbox, 1, 5, 1, 1)
        self.layout.addWidget(self.encrypt_for_me_label, 1, 6, 1, 3)
        self.layout.addWidget(self.recipients_label, 2, 5, 1, 2)
        self.layout.addWidget(self.recipients_list, 2, 7, 1, 4)
        self.layout.addWidget(self.select_recipient, 2, 11, 1, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
