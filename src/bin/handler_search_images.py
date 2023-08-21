from PySide6.QtCore import Qt, QUrl, QStandardPaths, QSize, Signal
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
    QProgressBar,
)
import sys
import os


class search_images(QWidget):
    finishedSearching = Signal(list)

    def __init__(self, import_path=None):
        super().__init__()
        self.import_path = import_path
        self.file_list = []
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)
        self.first_search = True

        font_header = QFont()
        font_header.setPointSize(20)

        # self.label_file_amount_label = QLabel(self)
        # self.label_file_amount_label.setText("Current Amount:")
        # self.label_file_amount_label.setAlignment(Qt.AlignCenter)
        # self.label_file_amount_label.setFont(font_header)
        # vbox.addWidget(self.label_file_amount_label)

        self.label_file_amount = QLabel(self)
        self.label_file_amount.setFont(font_header)
        self.label_file_amount.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.label_file_amount)


        self.label_current_folder_label = QLabel(self)
        self.label_current_folder_label.setText("Current folder:")
        self.label_current_folder_label.setAlignment(Qt.AlignCenter)
        self.label_current_folder_label.setFont(font_header)
        vbox.addWidget(self.label_current_folder_label)

        self.label_current_folder = QLabel(self)
        self.label_current_folder.setFont(font_header)
        self.label_current_folder.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.label_current_folder)


        self.label_current_file_label = QLabel(self)
        self.label_current_file_label.setText("Current File:")
        self.label_current_file_label.setAlignment(Qt.AlignCenter)
        self.label_current_file_label.setFont(font_header)
        vbox.addWidget(self.label_current_file_label)

        self.label_curret_file = QLabel(self)
        self.label_curret_file.setFont(font_header)
        self.label_curret_file.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.label_curret_file)

        # self.label.setFont(font_header)
        # self.label.setAlignment(Qt.AlignCenter)
        # self.label.setMinimumHeight(250)

        self.setLayout(vbox)
        self.setMaximumSize(850,590)
        # self.setFixedSize(300, 250)

    def get_file_list(self, import_path): # TODO Make this a seperate process, this hangs the program.
        directory = import_path
        file_amount = 0
        exclude_folders = set([".thumbnails", "cache", "Android"])
        # FUTURE Add Video files too!!!!
        filetypes_to_import = set(
            [
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".tiff",
                ".webp",
                ".svg",
                ".raw",
            ]
        )
        # ".ico",
        # ".mp4",
        # ".mov",
        # ".avi",
        # ".mkv",
        # ".wmv",
        # ".flv",
        # ".3gp",
        # ".mpeg",
        # ".mpg",
        # ".m4v",
        # ".vob",
        # ".m2v",
        # ".ts",
        # ".mts",
        # ".mxf",
        # ".webm",
        # ".ogv",
        # ".qt",
        # ".rm",
        # ".rmvb",
        # ".asf",

        for path, subdirs, fname in os.walk(directory["drive_path"]):
            # Exclude some folders, such as cache and thumbnail folders.
            self.label_current_folder.setText(f"{path}")
            subdirs[:] = [d for d in subdirs if d not in exclude_folders]

            for name in fname:
                # temp = name.split(".")[-1]
                if f'.{name.split(".")[-1].lower()}' not in filetypes_to_import:
                    continue
                file_amount = file_amount + 1
                file_path = os.path.join(path, name) # TODO Consider dict?
                file_name = name
                try:
                    file_date = os.path.getmtime(file_path)
                except OSError as e:
                    file_date = 0
                    pass
                self.file_list.append((file_path, file_date, file_name))
                # self.pbar.setValue(i + 1)
                self.label_file_amount.setText(f"Files found: {file_amount}")
                self.label_curret_file.setText(f"{file_name}")
                QApplication.processEvents()
        self.file_list = sorted(self.file_list, key=lambda x: x[1])
        
        if len(self.file_list) == 0 and self.first_search:
            self.first_search = False
            self.get_file_list(import_path)
            
        self.finishedSearching.emit(self.file_list)

        # return
        # for i, fname in enumerate(os.listdir(directory)):
        #     self.files_list.append(os.path.join(directory, fname))
        #     # self.pbar.setValue(i + 1)
        #     self.label.setText(f'Files found: {i + 1}')
        #     QApplication.processEvents()

    # def exec_(self):
    #     super().exec_()
    # return self.files_list


# def load_images(import_path):
#     app = QApplication(sys.argv)
#     loading_dialog = Dialog(import_path)
#     list_of_files = loading_dialog.get_file_list()
#     # sys.exit(Dialog(import_path).exec_())
#     return list_of_files


# load_images(import_path="K://")
