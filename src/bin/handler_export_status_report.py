# import json
# import sys
from PySide6.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QLabel,
    QCheckBox,
    QRadioButton,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QButtonGroup,
    QWidget,
)
from PySide6.QtCore import Qt, Signal, QObject, QEventLoop

# from bin.handle_settings import SettingsHandlerClass
# from datetime import datetime


class Export_status_report(QMainWindow):
    importMorePicturesSignal = Signal()

    def __init__(self, export_status):
        super().__init__()
        self.export_status = export_status

        self.setWindowTitle("Super Simple Image Importer")


        # Opprett hovedlayout
        layout = QVBoxLayout()

        self.statusLabel = QLabel()
        if self.export_status:
            self.statusLabel.setText("Export Successfull!")


        self.statusLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.statusLabel)

        self.importMoreButton = QPushButton("Importer flere bilder")
        self.importMoreButton.clicked.connect(self.importMore)
        # self.importMoreButton.setText("Importer flere bilder")
        layout.addWidget(self.importMoreButton)
    
        
        
        self.exitButton = QPushButton()
        self.exitButton.clicked.connect(QApplication.quit)
        self.exitButton.setText("Exit Program")
        layout.addWidget(self.exitButton)

        # TODO "Åpne mappe" Knapp

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def importMore(self):
        self.importMorePicturesSignal.emit()
        print()
