from PySide6.QtCore import (
    Qt,
    QUrl,
    QStandardPaths,
    QTimer,
    QSize,
    QFileInfo,
    QPointF,
    QItemSelection,
    QRect,
    # pyqtSignal,
    Signal,
    QThread,
    QRectF,
    QRunnable,
    # pyqtSlot,
    QThreadPool,
    QObject,
    Slot,
    QEventLoop,
)
from PySide6.QtGui import (
    QImageReader,
    QPixmap,
    QIcon,
    QFontMetrics,
    QPainter,
    QPen,
    QColor,
    QPainterPath,
    QImage,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QSizePolicy,
    QApplication,
    QDialog,
    QFileDialog,
    QFileIconProvider,
    QFrame,
    QGraphicsWidget,
    QGraphicsScene,
    QHBoxLayout,
    QLabel,
    QListView,
    QListWidget,
    QListWidgetItem,
    QGraphicsView,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionFocusRect,
    QVBoxLayout,
    QWidget,
    QScrollArea,
    QSlider,
    # qApp,
)
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest

import sys
import os
import time
import subprocess
import argparse

# import debugpy

from bin.update_check import check_for_updates
from bin.handler_import_path import widget_select_device
from bin.handler_search_images import search_images

# from bin import handler_MTP # DISABLE MTP
from bin.handler_get_removable_drives import fetch_devices
from bin.handler_select_images_to_import import Gallery_Select
from bin.handler_export import Export_jobs_widget
from bin.handler_work_queue import Work_queue
from bin.handler_export_status_report import Export_status_report
from bin.debug_write import isDebug, writeDebug
from bin.handler_worker_queue_file import worker_queue_file_handler



class Signals(QObject):
    finished = Signal()


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("Super Simple Image Importer")
        self.resize(800, 600)
        self.setMaximumSize(900, 600)

        self.section_space_layout = QHBoxLayout()

        # selectButton = QPushButton("Select")

        # layout = QVBoxLayout()
        # layout.addWidget(selectButton)

        centralWidget = QWidget()
        centralWidget.setLayout(self.section_space_layout)
        self.setCentralWidget(centralWidget)

        self.change_layout("import_path_module")

    def closeEvent(self, event):
        try:
            if isDebug():
                subprocess.Popen(
                    ["taskkill", "/F", "/IM", "mtpmount-x64.exe"],
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                )
            else:
                subprocess.Popen(
                    ["taskkill", "/F", "/IM", "mtpmount-x64.exe"],
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )

        except subprocess.CalledProcessError:
            pass
        event.accept()

    # Definer en funksjon for å fortsette etter at signalet er utløst
    def done_selecting_device(self, selected_device):
        FolderPath = ""

        if selected_device["device_id"] == "PC":
            # Let user select folder
            initial_dir = os.path.expanduser("~/Pictures")
            FolderPath = str(
                QFileDialog.getExistingDirectory(
                    self, "Vennligst velg mappe du vil importere fra", initial_dir
                )
            )
            if FolderPath == "":
                return
            
        # Handle returned path from user.
        self.mounted_import_path = {
            "drive_letter": selected_device["device_path_pretty"],
            "drive_name": selected_device["device_name"],
            "drive_path": selected_device["device_path"],
        }


        if (
            self.mounted_import_path is not None
        ):  # BUG Something is happening here that makes it use long time to go to the next screen.
            self.change_layout("handler_search_images")
            # loaded_images = handler_search_images.load_images(mounted_import_path)
        elif self.mounted_import_path is None:
            pass

        # Before disabling MTP:
        # if selected_device["device_id"] == "PC":
        #     FolderPath = ""
        #     initial_dir = os.path.expanduser("~/Pictures")
        #     FolderPath = str(QFileDialog.getExistingDirectory(self, "Vennligst velg mappe du vil importere fra", initial_dir))
        #     if FolderPath == "":
        #         return
        #     drive_letter = FolderPath.split(":")[0]
        #     drive_name = FolderPath.split("/")[-1]
        #     drive_path = FolderPath
        #     self.mounted_import_path = {'drive_letter': drive_letter, 'drive_name': drive_name, 'drive_path': drive_path}

        #     # debugPath = f"{os.path.join(os.environ['USERPROFILE'], 'Pictures')}"
        #     # self.mounted_import_path = {'drive_letter': 'C', 'drive_name': 'MineBilder', 'drive_path': debugPath}

        # else:
        #     self.mounted_import_path = handler_MTP.mount_MTP_device(selected_device)

        # if self.mounted_import_path is not None: # BUG Something is happening here that makes it use long time to go to the next screen.
        #     self.change_layout("handler_search_images")
        #     # loaded_images = handler_search_images.load_images(mounted_import_path)
        # elif self.mounted_import_path is None:
        #     pass

    def done_searching_for_files(self, file_list):
        self.file_list = file_list
        self.change_layout("handler_select_images_to_import")

        # print()

    def done_selecing_images(self, file_list_import):
        self.file_list_import = file_list_import
        self.change_layout("handler_export")

        # print(file_list)
        # print(file_list)

    def start_job_queue(self, jobQueue):
        self.job_queue = jobQueue
        self.change_layout("handler_work_queue")

        # print(jobQueue)

    def job_queue_finished(self, export_status):
        self.export_status = export_status
        writeDebug("Start Queue Clicked and registered!")
        self.change_layout("handler_export_status_report")

    def importMoreImages(self):
        self.change_layout("handler_select_images_to_import")

    def change_layout(self, newLayout):
        if newLayout == "import_path_module":
            self.new_module = widget_select_device()
            # Koble signalet til funksjonen
            self.new_module.importPathSelected.connect(self.done_selecting_device)

        elif newLayout == "handler_search_images":
            self.new_module = search_images()  # self.mounted_import_path
            # Koble signalet til funksjonen
            self.new_module.finishedSearching.connect(self.done_searching_for_files)

        elif newLayout == "handler_select_images_to_import":
            self.new_module = Gallery_Select()  # self.mounted_import_path
            # Koble signalet til funksjonen
            self.new_module.signal_done_selecting.connect(self.done_selecing_images)

        elif newLayout == "handler_export":
            self.new_module = Export_jobs_widget(self.file_list_import)
            # Koble signalet til funksjonen
            self.new_module.start_import_signal.connect(self.start_job_queue)

        elif newLayout == "handler_work_queue":
            self.new_module = Work_queue()
            # Koble signalet til funksjonen
            self.new_module.finished_work_queue.connect(self.job_queue_finished)

        elif newLayout == "handler_export_status_report":
            self.new_module = Export_status_report(self.export_status)
            # Koble signalet til funksjonen
            self.new_module.importMorePicturesSignal.connect(self.importMoreImages)

        else:
            # self.new_module = self.ErrorLayout()
            writeDebug("Error")

        # Common settings:
        self.new_module.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setCentralWidget(self.new_module)

        if newLayout == "handler_search_images":
            self.new_module.get_file_list(self.mounted_import_path)

        elif newLayout == "handler_select_images_to_import":
            self.new_module.start_item_import(self.file_list)

        elif newLayout == "handler_work_queue":
            self.new_module.start_working(self.job_queue)


if __name__ == "__main__":
    # Reset some stuff
    # MTPenabled = False

    # handler_MTP.unmount_MTP_device(unmount_all_debug=True if isDebug() else False) # DISABLE MTP

    worker_queue_file_handler.delete()

    # try:
    #     os.remove("WorkQueue.json")
    # except FileNotFoundError as e:
    #     pass

    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "-forceUpdate", action="store_true", help="Force update the program."
    )
    args = parser.parse_args()

    app = QApplication([])

    is_update_available = check_for_updates()
    # is_update_available = [False]

    if is_update_available[0] or args.forceUpdate:
        from bin.fetch_and_install_update import download_and_install_latest_release

        download_and_install_latest_release(
            local_ver=is_update_available[1], remote_ver=is_update_available[2]
        )

    window = MainWindow()
    window.show()
    app.exec()
