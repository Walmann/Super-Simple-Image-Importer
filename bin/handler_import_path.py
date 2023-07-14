from PySide6.QtCore import Qt, QUrl, QStandardPaths, QSize, QEventLoop, Signal, QObject
from PySide6.QtGui import QImageReader, QPixmap, QIcon, QFont
from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QListWidgetItem,
    QDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QApplication,
    QWidget,
    QLayout,
)
import sys

import handler_MTP

# class Signals(QObject):
#     finished = Signal()
# class widget_select_device(QDialog):
class widget_select_device(QWidget):
    
    
    # Setup Signals
    importPathSelected = Signal(dict)



    def __init__(self, devices_list=None, parent=None):
        super(widget_select_device, self).__init__().__init__(parent)

        # self.Device_selected_signal = Signal()
        self.button_pressed = None
        self.event_loop = QEventLoop()

        devices_list = handler_MTP.fetch_devices()

        # Main Window
        vbox = QVBoxLayout()

        # Create fonts
        font_header = QFont()
        font_header.setPointSize(20)

        # Lag Header
        # label = QLabel("Importer fra:")
        self.label = QLabel("Velg hvor du skal importere fra")
        self.label.setFont(font_header)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setMinimumHeight(250)

        vbox.addWidget(self.label)

        # availableDevices = fetch_devices()

        vboxMTPLayout = QVBoxLayout()

        # Add folder on computer into devices_list
        devices_list["Folder"] = {}
        devices_list["Folder"]["device_name"] = "Importer fra datamaskin"
        devices_list["Folder"]["device_id"] = "PC"

        for devices in devices_list:
            self.device = devices_list[devices]
            self.device_button = QPushButton()
            self.device_button.setText(self.device["device_name"])
            self.device_button.clicked.connect(self.handle_import)
            self.device_button.setStyleSheet("padding:50px")
            vboxMTPLayout.addWidget(self.device_button)

        # BUG if there are too many devices, the widget ingores size constrains of parentwidget.
        # devices_list["Folder2"] = {}
        # devices_list["Folder2"]["device_name"] = "Importer fra datamaskin"
        # devices_list["Folder2"]["device_id"] = "PC"
        # devices_list["Folder4"] = {}
        # devices_list["Folder4"]["device_name"] = "Importer fra datamaskin"
        # devices_list["Folder4"]["device_id"] = "PC"
        # devices_list["Folder3"] = {}
        # devices_list["Folder3"]["device_name"] = "Importer fra datamaskin"
        # devices_list["Folder3"]["device_id"] = "PC"

        vbox.addLayout(vboxMTPLayout)

        # Cancel
        btn_cancel = QPushButton("Avbryt")
        btn_cancel.clicked.connect(self.cancel)
        btn_cancel.setStyleSheet("padding:50px")
        vbox.addWidget(btn_cancel)

        self.setLayout(vbox)

    def handle_import(self):
        # self.button_pressed = self.device
        self.importPathSelected.emit(self.device)
        # self.emit(self.button_pressed)
        # return self.button_pressed
        # self.event_loop.quit()

    def cancel(self):
        self.button_pressed = "cancel"
        exit(self.button_pressed)
        # self.event_loop.quit()

    # def exec_(self):
    #     if self.button_pressed is None:
    #         super().exec_()
    #         self.event_loop.exec_()
    #     else:
    #         return self.button_pressed


# def select_device():
#     app = QApplication(sys.argv)
#     selected_device = widget_select_device().exec()
#     # selected_device = widget_select_device().exec_()
#     return selected_device


# select_device()


# select_device()


# from PyQt5.QtCore import Qt, QUrl, QStandardPaths, QSize
# from PyQt5.QtGui import QImageReader, QPixmap, QIcon
# from PyQt5.QtWidgets import (
#     QMainWindow,
#     QFileDialog,
#     QListWidgetItem,
#     QDialog,
#     QLabel,
#     QVBoxLayout,
#     QHBoxLayout,
#     QPushButton,
#     QApplication,
#     QWidget,
# )
# import sys

# import handler_MTP


# class widget_select_device(QDialog):
#     def __init__(self, devices_list=None):
#         super().__init__()

#         self.button_pressed = None

#         devices_list = handler_MTP.fetch_devices()

#         # Main Window
#         vbox = QVBoxLayout()
#         label = QLabel("Importer fra:")
#         vbox.addWidget(label)

#         # availableDevices = fetch_devices()
#         vboxMTP = QVBoxLayout()

#         # Add folder on computer into devices_list
#         devices_list["Folder"] = {}
#         devices_list["Folder"]["device_name"] = "Importer fra datamaskin"
#         devices_list["Folder"]["device_id"] = "PC"


#         for devices in devices_list:
#             self.device = devices_list[devices]
#             self.device_button = QPushButton()
#             self.device_button.setText(self.device["device_name"])
#             self.device_button.clicked.connect(
#                 lambda checked, text=self.device: self.handle_import(text)
#             )
#             self.device_button.setStyleSheet("padding:50px")
#             vboxMTP.addWidget(self.device_button)

#         vbox.addLayout(vboxMTP)

#         # Cancel
#         btn_cancel = QPushButton("Avbryt")
#         btn_cancel.clicked.connect(self.cancel)
#         btn_cancel.setStyleSheet("padding:50px")
#         vbox.addWidget(btn_cancel)

#         self.setLayout(vbox)

#     def handle_import(self, device):
#         self.button_pressed = device
#         self.accept()

#     def cancel(self):
#         self.button_pressed = "cancel"
#         self.reject()

#     def exec_(self):
#         super().exec_()
#         return self.button_pressed


# def select_device():
#     app = QApplication(sys.argv)
#     selected_device = widget_select_device().exec_()
#     return selected_device

# # select_device()
