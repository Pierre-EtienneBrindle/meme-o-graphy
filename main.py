import sys
import os
import gzip

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QTabWidget, QWidget, QCheckBox, QLabel, QComboBox, QFileDialog,QListWidget, QMessageBox
from PyQt6.QtGui import QPixmap
from PIL import Image
from Images.ImageLossy import ImageLossy
import gnupg


gpg = gnupg.GPG()
script_dir = os.path.dirname(__file__)
print(script_dir)

class EncodeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.constructEncodeTab()

    def constructEncodeTab(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.display = QLabel()
        self.pixmap = QPixmap(os.path.join(script_dir, "welcome_broccoli.png"))
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
        errorMessage = []
        if self.selected_image_path == "":
            errorMessage.append("no image selected")
        if self.outputed_file_path == "":
            errorMessage.append("no output file path")
        if self.selected_file_path == "":
            errorMessage.append("no selected file path")

        if len(errorMessage) != 0:
            popup = QMessageBox(self)
            popup.setWindowTitle("Warning")
            msg = ""
            for message in errorMessage :
                msg += message
                
            popup.setText(msg)
            popup.setIcon(QMessageBox.Icon.Critical)
            popup.exec()
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
            image = ImageLossy.fromPILImage(Image.open(self.selected_image_path).copy())
            image = image.encode(compressed_data)
            image.save(self.outputed_file_path)

class DecodeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.constructDecodeTab()

    def constructDecodeTab(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.display = QLabel()
        self.pixmap = QPixmap("/tmp/image.png")
        self.display.setPixmap(self.pixmap)
        self.display.resize(200, 200)

        self.select_image_button = QPushButton("Select image")
        self.select_image_button.clicked.connect(self.selectImageButtonClicked)
        self.selected_image_label = QLabel("No image selected")
        self.selected_image_path = ""

        self.output_file_button = QPushButton("Select output")
        self.output_file_button.clicked.connect(self.selectOutputFileButtonClicked)
        self.outputed_file_label = QLabel("No file selected")
        self.outputed_file_path = ""

      
        self.decode_button = QPushButton("Decode")
        self.decode_button.clicked.connect(self.decodeButtonClicked)

        self.layout.addWidget(self.select_image_button, 0, 0, 1, 1)
        self.layout.addWidget(self.selected_image_label, 0, 1, 1, 2)
        self.layout.addWidget(self.output_file_button, 0, 6, 1, 1)
        self.layout.addWidget(self.outputed_file_label, 0, 7, 1, 2)
        self.layout.addWidget(self.display, 1, 0, 19, 20)
        self.layout.addWidget(self.decode_button, 13, 20, 1, 5)

    def selectImageButtonClicked(self):
        self.selected_image_path = QFileDialog.getOpenFileName(self, "Open file")[0]
        self.selected_image_label.setText(os.path.basename(os.path.normpath(self.selected_image_path)))

        self.pixmap = QPixmap(self.selected_image_path)
        self.display.setPixmap(self.pixmap)

    def selectOutputFileButtonClicked(self):
        self.outputed_file_path = QFileDialog.getOpenFileName(self, "Open file")[0]
        self.outputed_file_label.setText(os.path.basename(os.path.normpath(self.outputed_file_path)))


    def decodeButtonClicked(self):
        if self.selected_image_path == "" or self.outputed_file_path == "" :
            return

        image = ImageLossy.fromPILImage(Image.open(self.selected_image_path).copy())
        data = image.decode()
        decompressed_data = gzip.decompress(data)

        decrypted_data = gpg.decrypt(decompressed_data)
        if decrypted_data.ok == False:
            print("alert!!!")
            return

        with open(self.outputed_file_path, "wb") as file :
            file.write(decrypted_data.data)




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("meme-o-graphy")
        self.showMaximized()

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.encode_tab = EncodeTab()
        self.tab_widget.addTab(self.encode_tab, "Encode")
        self.decode_tab = DecodeTab()
        self.tab_widget.addTab(self.decode_tab, "Decode")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
