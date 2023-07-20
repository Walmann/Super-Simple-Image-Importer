import pathlib
import shutil
import json
import sys
from datetime import datetime
from PIL import Image
from os.path import splitext as PathSplitText
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
        for index , job in enumerate(work_queue):
            self.countInt.setText(f"{index +1} / {len(work_queue)}")
            jobEntry = work_queue[job]
            self.handle_job(job=jobEntry)


    def createFilePath(self, job):
        
        # FUTURE Add Export folder.
        prefix = os.path.join(os.environ["USERPROFILE"], "Pictures")
        
        fullUrl = os.path.join(prefix)
        dateTimeSorting = datetime.now().strftime(job['FolderStructureSelection'])

        if job["FolderStructureNamingMethod"] == "subFolders":
            fullUrl = os.path.join(prefix, dateTimeSorting.replace("-","\\"), job['FolderName'])
        elif job["FolderStructureNamingMethod"] == "direct":
            fullUrl = os.path.join(prefix, dateTimeSorting, job['FolderName'])
        
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

            #Convert image to PNG
            if job["ConvertImageToPng"]:
                newFilePath = self.convert_to_png(newFilePath)

            if type(job["ResizeNewSize"] ) == int:
                self.resizeImage(resolution=job["ResizeNewSize"],image_path=newFilePath)
                # self.resizeImage(self, image_path=newFilePath, resolution=job["ResizeNewSize"])

            self.progressBar.setValue(i)            
        
        self.progressBar.setValue(len(job["FilesToImport"]))            
        self.finished_work_queue.emit(True)

    def convert_to_png(self, image_path):
        image = Image.open(image_path)
        new_image_path = PathSplitText(image_path)[0] + '.png'
        image.save(new_image_path)
        return new_image_path
    
    def resizeImage(self, image_path, resolution):
        # Load the image
        image = Image.open(image_path)

        # Get the width and height of the image
        width, height = image.size

        # Determine the aspect ratio of the image
        aspect_ratio = width / height

        # Parse the size string into width and height integers
        # size_parts = resolution.split("x")
        # max_width = int(size_parts[0])
        # max_height = int(size_parts[1])
        max_width = resolution
        max_height = resolution

        # Determine the maximum width and height based on the size parameters
        if aspect_ratio >= 1:
            # Landscape orientation
            new_width = min(width, max_width)
            new_height = int(new_width / aspect_ratio)
            if new_height > max_height:
                new_height = max_height
                new_width = int(new_height * aspect_ratio)
        else:
            # Portrait orientation
            new_height = min(height, max_height)
            new_width = int(new_height * aspect_ratio)
            if new_width > max_width:
                new_width = max_width
                new_height = int(new_width / aspect_ratio)

        # Resize the image using the calculated width and height
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        resized_image.save(image_path)
        return resized_image