import sys
import os
import gzip

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QCheckBox, QLabel, QComboBox, QFileDialog, QListWidget
from PyQt6.QtGui import QPixmap
from PIL import Image
import gnupg


gpg = gnupg.GPG()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("meme-o-graphy")
        self.showMaximized()

        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.layout = QGridLayout()
        self.widget.setLayout(self.layout)

        self.display = QLabel()
        self.pixmap = QPixmap("/tmp/image.png")
        self.display.setPixmap(self.pixmap)
        self.display.resize(200, 200)

        self.select_image_button = QPushButton("Select image")
        self.select_image_button.clicked.connect(self.selectImageButtonClicked)
        self.selected_image_label = QLabel("No image selected")
        self.selected_image_path = ""

        self.select_file_button = QPushButton("Select input")
        self.select_file_button.clicked.connect(self.selectInputFileButtonClicked)
        self.selected_file_label = QLabel("No file selected")
        self.selected_file_path = ""

        self.output_file_button = QPushButton("Select output")
        self.output_file_button.clicked.connect(self.selectOutputFileButtonClicked)
        self.outputed_file_label = QLabel("No file selected")
        self.outputed_file_path = ""

        self.sign_checkbox = QCheckBox()
        self.sign_label = QLabel("Sign message")
        self.encrypt_for_me_checkbox = QCheckBox()
        self.encrypt_for_me_label = QLabel("Encrypt for me")
        self.recipients_label = QLabel("Select recipients")
        self.recipients_list = QComboBox()
        self.recipients_list.addItems(map(lambda x: x["uids"][0], gpg.list_keys()))
        self.selected_recipients_list = QListWidget()
        self.select_recipient = QPushButton("Add")
        self.select_recipient.clicked.connect(self.selectRecipientButtonClicked)
        self.remove_recipient_button = QPushButton("Remove recipient")
        self.remove_recipient_button.clicked.connect(self.removeRecipientButtonClicked)
        self.encode_button = QPushButton("Encode")
        self.encode_button.clicked.connect(self.encodeButtonClicked)

        self.layout.addWidget(self.select_image_button, 0, 0, 1, 1)
        self.layout.addWidget(self.selected_image_label, 0, 1, 1, 2)
        self.layout.addWidget(self.select_file_button, 0, 3, 1, 1)
        self.layout.addWidget(self.selected_file_label, 0, 4, 1, 2)
        self.layout.addWidget(self.output_file_button, 0, 6, 1, 1)
        self.layout.addWidget(self.outputed_file_label, 0, 7, 1, 2)
        self.layout.addWidget(self.display, 1, 0, 19, 20)

        self.layout.addWidget(self.sign_label, 0, 20, 1, 1)
        self.layout.addWidget(self.sign_checkbox, 0, 21, 1, 1)
        self.layout.addWidget(self.encrypt_for_me_label, 1, 20, 1, 1)
        self.layout.addWidget(self.encrypt_for_me_checkbox, 1, 21, 1, 1)
        self.layout.addWidget(self.recipients_label, 2, 20, 1, 1)
        self.layout.addWidget(self.recipients_list, 3, 20, 1, 4)
        self.layout.addWidget(self.select_recipient, 3, 24, 1, 1)
        self.layout.addWidget(self.selected_recipients_list, 4, 20, 8, 5)
        self.layout.addWidget(self.remove_recipient_button, 12, 20, 1, 5)
        self.layout.addWidget(self.encode_button, 13, 20, 1, 5)

    def selectImageButtonClicked(self):
        self.selected_image_path = QFileDialog.getOpenFileName(self, "Open file")[0]
        self.selected_image_label.setText(os.path.basename(os.path.normpath(self.selected_image_path)))

        self.pixmap = QPixmap(self.selected_image_path)
        self.display.setPixmap(self.pixmap)

    def selectInputFileButtonClicked(self):
        self.selected_file_path = QFileDialog.getOpenFileName(self, "Open file")[0]
        self.selected_file_label.setText(os.path.basename(os.path.normpath(self.selected_file_path)))

    def selectOutputFileButtonClicked(self):
        self.outputed_file_path = QFileDialog.getOpenFileName(self, "Open file")[0]
        self.outputed_file_label.setText(os.path.basename(os.path.normpath(self.outputed_file_path)))

    def selectRecipientButtonClicked(self):
        self.selected_recipients_list.addItem(self.recipients_list.currentText())
        self.recipients_list.removeItem(self.recipients_list.currentIndex())

    def removeRecipientButtonClicked(self):
        if self.selected_recipients_list.currentItem() != None:
            self.recipients_list.addItem(self.selected_recipients_list.currentItem().text())
            self.selected_recipients_list.takeItem(self.selected_recipients_list.currentIndex().row())

    def encodeButtonClicked(self):
        if self.selected_image_path == "" or self.outputed_file_path == "" or self.selected_image_path == "":
            return

        with open(self.selected_file_path, "r") as file:
            content = file.read()

        recipients = []
        for _ in range(self.selected_recipients_list.count()):
            recipients.append(self.selected_recipients_list.takeItem(0).text())
        self.selected_recipients_list.addItems(recipients)

        result = gpg.encrypt(content, recipients=recipients, always_trust=True, armor=False)
        if result.ok:
            compressed_data = gzip.compress(result.data)
            image = ImageLossy.fromPILImage(Image.open(self.selected_image_path))
            image = image.encode(compressed_data)
            image.save(self.outputed_file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
