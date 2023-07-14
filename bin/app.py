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
import debugpy


from handler_import_path import widget_select_device
# import handler_import_path
from handler_search_images import search_images
import handler_MTP
# import handler_select_images_to_import
from handler_select_images_to_import import Gallery_Select
from handler_export import Export_jobs_widget
from handler_work_queue import Work_queue
from handler_export_status_report import Export_status_report


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


        # self.start_app_process()
        print()


    # Definer en funksjon for å fortsette etter at signalet er utløst
    def done_selecting_device(self, selected_device):
    
        if selected_device["device_id"] == "PC":
            
            # FUTURE Get Folder selector thing here!
            print( "TODO Get Folder selector thing here.")
        else:
            self.mounted_import_path = handler_MTP.mount_MTP_device(selected_device)

        if self.mounted_import_path is not None:
            self.change_layout("handler_search_images")
            # loaded_images = handler_search_images.load_images(mounted_import_path)

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
        self.change_layout("handler_export_status_report")

    def change_layout(self, newLayout):     


        if newLayout == "import_path_module":
            self.new_module = widget_select_device()
            # Koble signalet til funksjonen
            self.new_module.importPathSelected.connect(self.done_selecting_device)

        
        elif newLayout == "handler_search_images":
            self.new_module = search_images() # self.mounted_import_path
            # Koble signalet til funksjonen
            self.new_module.finishedSearching.connect(self.done_searching_for_files)
        
        
        elif newLayout == "handler_select_images_to_import":
            self.new_module = Gallery_Select() # self.mounted_import_path
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
            # self.new_module.start_import_signal.connect(self.start_job_queue)
            
        else: 
            # self.new_module = self.ErrorLayout()
            print("Error")



        # Common settings: 
        self.new_module.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.setCentralWidget(self.new_module)


        if newLayout == "handler_search_images":
            self.new_module.get_file_list(self.mounted_import_path)
            
        elif newLayout == "handler_select_images_to_import":
            self.new_module.start_item_import(self.file_list)

        elif newLayout == "handler_work_queue":
            self.new_module.start_working(self.job_queue)




    # def select_device():
    #     # Choose Directory / Path:
    #     selected_device = handler_import_path.select_device()
    #     # For debugging:
    #     # selected_device = {'device_name': 'HUAWEI P30 Pro', 'device_id': '1', 'device_subname': 'Storage Intern lagring'}

    # if selected_device["device_id"] == "PC":
    #     # mounted_import_path = {'drive_letter': 'C', 'drive_name': 'MineBilder', 'drive_path': r'C:\Users\tov\Pictures'}
    #     mounted_import_path = {'drive_letter': 'C', 'drive_name': 'MineBilder', 'drive_path': r'C:\Users\tov\Pictures\Bilder Etter dato'}
    #     # FUTURE Get Folder selector thing here!
    #     print( "TODO Get Folder selector thing here.")
    # else:
    #     mounted_import_path = handler_MTP.mount_MTP_device(selected_device)

    # if mounted_import_path is not None:
    #     loaded_images = handler_search_images.load_images(mounted_import_path)

    # if loaded_images is not None:
    #     images_to_import = handler_select_images_to_import.start(loaded_images)
    #     # handler_select_images_to_import.start(file_list)

    ###### TODO STILL NEED TO BE IMPORTED ######
    # if images_to_import is not None:
    #     export_jobs = handler_export.start(images_to_import)

    print()

if __name__ == "__main__":
    # Reset some stuff
    # handler_MTP.unmount_MTP_device(selected_device)
    try:
        os.remove("WorkQueue.json")
    except FileNotFoundError as e:
        pass



    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()



# class MainApp(QApplication):
#     def __init__(self, sys_argv):
#         super().__init__(sys_argv)
#         self.initializeApplication()

#     def initializeApplication(self):
#         self.window = MainWindow()  # Create an instance of MainWindow
#         self.window.show()


# if __name__ == "__main__":
#     app = MainApp(sys.argv)
#     sys.exit(app.exec())


# def start():
#     # # Reset some stuff
#     # handler_MTP.unmount_MTP_device()
#     # try:
#     #     os.remove("WorkQueue.txt")
#     # except FileNotFoundError as e:
#     #     pass

#     app = QApplication(sys.argv)
#     window = MainWindow().exec()
#     window.show()
# selected_device = Dialog().exec_()

# app = QApplication(sys.argv)
# window = MainWindow(file_list=file_list)
# window.show()
# # app.exec_()
# # selected_files = window.run()
# selected_files = window.waitForSelection()

# print("Selected files:", selected_files)
# app.quit()
# return selected_files


# start()


# selected_device = handler_import_path.select_device()

# # For debugging:
# # selected_device = {'device_name': 'HUAWEI P30 Pro', 'device_id': '1', 'device_subname': 'Storage Intern lagring'}


# # Reset some stuff
# handler_MTP.unmount_MTP_device(selected_device)
# try:
#     os.remove("WorkQueue.txt")
# except FileNotFoundError as e:
#     pass


# if selected_device["device_id"] == "PC":
#     # mounted_import_path = {'drive_letter': 'C', 'drive_name': 'MineBilder', 'drive_path': r'C:\Users\tov\Pictures'}
#     mounted_import_path = {'drive_letter': 'C', 'drive_name': 'MineBilder', 'drive_path': r'C:\Users\tov\Pictures\Bilder Etter dato'}
#     # FUTURE Get Folder selector thing here!
#     print( "TODO Get Folder selector thing here.")
# else:
#     mounted_import_path = handler_MTP.mount_MTP_device(selected_device)


# if mounted_import_path is not None:
#     loaded_images = handler_search_images.load_images(mounted_import_path)

# if loaded_images is not None:
#     images_to_import = handler_select_images_to_import.start(loaded_images)
#     # handler_select_images_to_import.start(file_list)

# if images_to_import is not None:
#     export_jobs = handler_export.start(images_to_import)

# # temp = images_to_import
print()
