import pathlib
import shutil
import json
import sys
from datetime import datetime

import os
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
    QProgressBar
)
from PySide6.QtCore import Qt, Signal, QObject, QEventLoop



# class Signals(QObject):
#     finished = Signal()





class Work_queue(QWidget):
    finished_work_queue = Signal(bool)
    def __init__(self):
        super().__init__()
        self.work_queue = {}
        
        layout = QVBoxLayout()
        

        # self.headerLabel = QLabel()
        # self.headerLabel.setText("Importing Images")
        # self.headerLabel.setAlignment(Qt.AlignCenter)
        # layout.addWidget(self.headerLabel)        
        
        
        self.infoBlock = QWidget()
        self.infoBlock_layout = QVBoxLayout()
        self.infoBlock.setLayout(self.infoBlock_layout)
        layout.addWidget(self.infoBlock)

        self.countText = QLabel()
        self.countText.setText("Importing job: ")
        self.countText.setAlignment(Qt.AlignCenter)
        self.infoBlock_layout.addWidget(self.countText)

        self.countInt = QLabel()
        self.countInt.setText("0 / 0")
        self.countInt.setAlignment(Qt.AlignCenter)
        self.infoBlock_layout.addWidget(self.countInt)

        self.progressBlock = QWidget()
        self.progressBlock_layout = QVBoxLayout()
        self.progressBlock.setLayout(self.progressBlock_layout)
        layout.addWidget(self.progressBlock)

        self.progressLabel = QLabel()
        self.progressLabel.setText("Current Progress: ")
        self.progressLabel.setAlignment(Qt.AlignCenter)
        self.progressBlock_layout.addWidget(self.progressLabel)        
        
        
        self.progressBar = QProgressBar()
        # self.progressBar.setGeometry(QRect(90, 230, 118, 23))
        self.progressBar.setValue(0)
        self.progressBlock_layout.addWidget(self.progressBar)

        self.setLayout(layout)


    def start_working(self, work_queue):
        print()
        for index , job in enumerate(work_queue): ##### TODO Foldername is missing!
            self.countInt.setText(f"{index +1} / {len(work_queue)}")
            jobEntry = work_queue[job]
            self.handle_job(job=jobEntry)


    def createFilePath(self, job):
        
        # FUTURE Add Export folder.
        prefix = os.path.join(os.environ["USERPROFILE"], "Pictures")
        
        fullUrl = os.path.join(prefix)

        if job["FolderStructureNamingMethod"] == "subFolders":
            dateTimeSorting = datetime.now().strftime(job['FolderStructureSelection'])
            fullUrl = os.path.join(prefix, dateTimeSorting, job['FolderName'])
        elif job["FolderStructureNamingMethod"] == "direct":
            fullUrl = os.path.join(prefix, job["FolderName"])
        
        return fullUrl


    def find_available_name_for_file(self, filename):
        i = 1
        while os.path.exists(filename):
            name, ext = os.path.splitext(filename)
            if '(' in name and ')' in name:
                name = name[:name.rfind('(')]
            filename = f"{name} ({i}){ext}"
            i += 1
        with open(filename, 'w') as f:
            pass
        return filename


    def handle_job(self, job=None):
        # Create folder structure: 
        folderPath = self.createFilePath(job)


        # Ordne med Progressbar
        self.progressBar.setMaximum(len(job["FilesToImport"]))

        for i, file in enumerate(job["FilesToImport"]):
            pathlib.Path(folderPath).mkdir(parents=True, exist_ok=True)
            oldFilePath = file[0]
            newFilePath = os.path.join(folderPath, file[2])

            if os.path.isfile(oldFilePath):
                newFilePath = self.find_available_name_for_file(newFilePath)
            shutil.copy2(oldFilePath, newFilePath)

            self.progressBar.setValue(i)            
        
        self.progressBar.setValue(len(job["FilesToImport"]))            
        self.finished_work_queue.emit(True)

