# Create window to select images that are going to be imported.

# from PyQt5.QtCore import (
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
    QEventLoop
    
)
# from PyQt5.QtGui import (
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
# from PyQt5.QtWidgets import (
from PySide6.QtWidgets import (
    QAbstractItemView,
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
from bin.debug_write import isDebug, writeDebug
# from PyQt5.uic import loadUiType
import sys
import os
import time

class ImageLoader:
    def __init__(self):
        self.manager = QNetworkAccessManager()
        self.reply = None
        self.loop = QEventLoop()

    def load_image(self, url):
        request = QNetworkRequest(QUrl(url))
        self.reply = self.manager.get(request)
        self.reply.readyRead.connect(self.handle_ready_read)
        self.reply.finished.connect(self.loop.quit)
        self.loop.exec_()

        data = self.reply.readAll()
        image = QImage.fromData(data)

        return image

    def handle_ready_read(self):
        pass


# def loadingThumbnailsTest(self, item):
#         def __init__(self, item):
#             super().__init__()
#             self.item = item
#         path = item.filePath
#         image = QImage(path)
#         # if image.isNull():
#         #     print(f"Failed to load image from {path}")
#         #     image = self.load_image_async(path)
#         #     print(f"Failed to load image from {path}")
#         # else:
#         thumbnail = image.scaled(80,80,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation,)
#         self.item.setThumbnail(thumbnail)
#         print("Created thumbnail.")


class WorkerLoadingThumbnails(QRunnable): # OLD ORIGINAL
    def __init__(self, item):
        super().__init__()
        self.item = item
        

    # @pyqtSlot()
    def run(self):
        '''
        Your code goes in this function
        '''
        # if item.thumbnail is None:
        path = self.item.filePath
        QImageReader.setAllocationLimit(0)
        image = QImage(path)
        thumbnail = image.scaled(80,80,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation,)
        self.item.setThumbnail(thumbnail)
        # print("Created thumbnail.")
        
        # self.thumbnails[path] = thumbnail
        
        # GridView.updateThumbnailsList(path=path, thumbnail=thumbnail)

        

# class WorkerLoadingThumbnails(QThread):
#     finished = Signal()  # Added Signal

#     def __init__(self, item):
#         super().__init__()
#         self.item = item

#     def run(self):
#         path = self.item.filePath
#         image = QImage(path)
#         while image.isNull():
#             image = QImage(path)
#             if path.endswith(".mp4"):
#                 break
#         thumbnail = image.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
#         self.item.setThumbnail(thumbnail)
#         print("Hello!!")
        
#         self.finished.emit()  # Emit the finished signal
#         pass





class WorkerLoadingItems(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(WorkerLoadingItems, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    # @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)
    # def __init__(self, item):
    #     super().__init__()
    #     self.item = item

    # @pyqtSlot()
    # def run(self):
    #     '''
    #     Your code goes in this function
    #     '''
    #     # if item.thumbnail is None:
    #     for filename in self.item:
    #         GridView.addGridItem(self, path=filename)





# Custom graphics item representing an item in the grid
class GridItem(QGraphicsWidget):
    def __init__(self, path, tSize, parent=None):
        super().__init__(parent)
        self.path = path
        self.thumbnailSize = tSize
        self.thumbnail = None
        self.selected = False

        self.filePath = self.path[0]
        self.date = self.path[1]
        self.filename = self.path[2]

        # TODO Optimize the rendering. When it loads it laggs.
        self.setCacheMode(QGraphicsWidget.DeviceCoordinateCache)

        # Enable hover events and set tooltip
        self.setAcceptHoverEvents(True)
        self.setToolTip(self.filePath)

        # Set placeholder Thumbnail
        self.thumbnail = QImage("Assets\icon.ico")

    def setThumbnail(self, thumbnail):
        self.thumbnail = thumbnail
        self.update()

    def boundingRect(self):
        return QRectF(0, 0, self.thumbnailSize, self.thumbnailSize)

    def mousePressEvent(self, event):
        self.selected = not self.selected
        self.update()
        event.accept()

    def setSelected(self, selected):
        self.selected = selected
        self.update()

    def shape(self):
        path = super().shape()
        # Define a custom shape by creating a QPainterPath and adding desired geometry
        custom_shape = QPainterPath()
        custom_shape.addRect(self.boundingRect())  # Custom clickable area
        path = custom_shape
        return path

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background
        if self.selected:
            painter.setBrush(QColor(200, 200, 255))
        else:
            painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(self.boundingRect())

        # Draw centered text at the bottom
        font = painter.font()
        font.setPointSize(10)  # Adjust the font size as needed
        painter.setFont(font)

        # Set the name of the item. If over X characters, shorten it and add "..." at the end.
        text = self.filename  # Text to be displayed
        if len(text) > 10:
            text = f"{text[:10].strip()}..."

        # Calculate the width and height of the text
        text_rect = painter.boundingRect(option.rect, Qt.AlignCenter, text)

        # Calculate the position to center the text horizontally
        text_x = (option.rect.width() - text_rect.width()) / 2

        # Calculate the position to place the text at the bottom vertically
        text_y = option.rect.height() - text_rect.height() + 10
        painter.drawText(option.rect.x() + text_x, option.rect.y() + text_y, text)

        # Draw thumbnail
        if self.thumbnail is not None:
            thumbnail_size_number = 80 * self.thumbnailSize / 100
            thumbnail_size = QSize(thumbnail_size_number,thumbnail_size_number)
            scaled_thumbnail = self.thumbnail.scaled(thumbnail_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

            # Calculate the position to center the thumbnail horizontally within the item's bounding rectangle
            image_x = option.rect.x() + (option.rect.width() - scaled_thumbnail.width()) / 2

            # Calculate the position to center the thumbnail vertically within the item's bounding rectangle
            # image_y = option.rect.y() + (option.rect.height() - scaled_thumbnail.height()) / 2
            image_y = 10

            painter.drawImage(QPointF(image_x, image_y), scaled_thumbnail)




# Custom graphics view widget with the grid layout
class GridView(QGraphicsView):
    def __init__(self, parent=None, main_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setScene(QGraphicsScene(self))
        
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHint(QPainter.Antialiasing)

        self. thumbnailSize = 150
        self.thumbnails = {}
        
        self.threadpool = QThreadPool()
        # self.threadpool = []
        
        self.threadpool.setMaxThreadCount(1)
        writeDebug("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateGrid()

    def updateGrid(self):
        sizeThing = self.thumbnailSize
        sceneRect = QRectF(self.viewport().rect())
        itemsPerRow = max(1, int(sceneRect.width() / sizeThing))
        margin = (sceneRect.width() - (itemsPerRow * sizeThing)) / (itemsPerRow + 1)
        x = margin
        y = 0
   
        for item in self.scene().items():
            if isinstance(item, GridItem):
                item.setPos(x, y)
                x += sizeThing + margin
                if x + sizeThing > sceneRect.width():
                    x = margin
                    y += sizeThing + margin
        self.setSceneRect(self.scene().itemsBoundingRect())

    def addGridItem(self, path):
        item = GridItem(path, tSize=self.thumbnailSize)
        self.scene().addItem(item)
        # self.updateGrid()

    def closeEvent(self, event):
        for thread in self.threadpool:
            thread.quit()
            thread.wait()
        super().closeEvent(event)


    # def closeEvent(self, event):
    #     # Stop the thread pool when the window is closed
    #     self.threadpool.clear()
    #     self.threadpool.waitForDone()
    #     # Call the base class closeEvent to perform default window closing actions
    #     super().closeEvent(event)

    # def loadThumbnails(self):
    #         for item in self.scene().items():
    #             if isinstance(item, GridItem):
    #                 if item.path[0] not in self.thumbnails:
    #                     thread = WorkerLoadingThumbnails(item=item)
    #                     thread.finished.connect(self.threadFinished)
    #                     self.threadpool.append(thread)
    #                     thread.start()

    def threadFinished(self):
        thread = self.sender()
        if thread is not None:
            thread.finished.disconnect(self.threadFinished)
            self.threadpool.remove(thread)
            thread.deleteLater()
    def loadThumbnails(self):
        try:
            for item in self.scene().items():
                if isinstance(item, GridItem):
                    if item.path[0] not in self.thumbnails:
                        # loadingThumbnailsTest(self, item)
                    
                        worker = WorkerLoadingThumbnails(item=item)
                        self.threadpool.start(worker)
        except Exception as e:
            writeDebug(e)        
                
    def stopThreadPool(self):
        for thread in self.threadpool:
            thread.quit()
            thread.wait()

    # def lazyLoadThumbnails(self):
    #     for item in self.scene().items():
    #         if isinstance(item, GridItem):
    #             if item.path not in self.thumbnails:
    #                 self.loadThumbnail(item)

    # def scrollContentsBy(self, dx, dy):
    #     super().scrollContentsBy(dx, dy)
    #     self.lazyLoadThumbnails()

    def clearSelection(self):
        for item in self.scene().items():
            if isinstance(item, GridItem):
                item.setSelected(False)

    def getSelectedItems(self):
        selectedItems = []
        for item in self.scene().items():
            if isinstance(item, GridItem) and item.selected:
                selectedItems.append(item.path)
        return selectedItems


# class Signals(QObject):
#     finished = Signal()

class Gallery_Select(QMainWindow):
    # selectedItemsChanged = pyqtSignal(list)
    signal_items_created = Signal()
    signal_done_selecting = Signal(list)
    signal_done_creating_main_ui = Signal(list)
    def __init__(self, file_list=()):
        super().__init__()

        
        # self.signal = Signals()
        # self.selectedSignal = Signals()
        # self.signal = Signal()
        self.addedItems = 0
        # file_list.reverse() # FUTURE Add sortings methods
        self.file_list = file_list

        self.selectedItems = []

        # Build the UI
        self.waitForImportLabel = QLabel("Genererer fremvisning")
        # self.setCentralWidget(self.waitForImportLabel)
        
        self.gridWidget = GridView(main_window=self)
        # self.grid_view = GridView(main_window=self)
        # self.gridWidget.setVisible(False)
        self.setCentralWidget(self.gridWidget)
        
        self.setWindowTitle("Grid Widget")
        self.resize(800, 600)

        self.threadpoolAddItems = QThreadPool()
        # self.threadpoolAddItems.setMaxThreadCount(1)
        
        writeDebug("Multithreading with maximum %d threads" % self.threadpoolAddItems.maxThreadCount())


        

        selectButton = QPushButton("Select")
        selectButton.clicked.connect(self.selectButtonClicked)

        layout = QVBoxLayout()
        layout.addWidget(self.waitForImportLabel)
        layout.addWidget(self.gridWidget)
        layout.addWidget(selectButton)
        
        
        self.signal_items_created.connect(self.gridWidget.loadThumbnails)
        

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)



    def start_item_import(self, file_list):
        # waitForUi = self.signal_done_creating_main_ui.connect(self.add_items_to_gallery)
        writeDebug("generating Items.")

        self.file_list = file_list
        start = time.time()
        for filename in self.file_list:
                # print("Generatin Item")
                self.gridWidget.addGridItem(filename)
                self.addedItems = self.addedItems+1
                self.waitForImportLabel.setText(f"Genererer bildegalleri: {self.addedItems}")
        temp = self.gridWidget.scene().items()
        self.gridWidget.updateGrid()
        stop = time.time()
        writeDebug(f"Elapsed Time: {stop - start}")
        self.signal_items_created.emit()
        # temp = self.gridWidget.scene().items()
        # print()

        


    # def selectButtonClicked(self):
    #     self.selectedItems = self.gridWidget.getSelectedItems()
    #     self.selectedItemsChanged.emit(self.selectedItems) 
    
    def selectButtonClicked(self):
        # print("Before clear: " + str(self.gridWidget.threadpool.activeThreadCount()))
        self.gridWidget.threadpool.clear()
        # print("After clear: " + str(self.gridWidget.threadpool.activeThreadCount()))
        self.selectedItems = self.gridWidget.getSelectedItems()
        self.signal_done_selecting.emit(self.selectedItems)


    def closeEvent(self, event):
        self.gridWidget.stopThreadPool()
        super().closeEvent(event)


