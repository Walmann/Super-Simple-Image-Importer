# from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QListWidgetItem
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5 import *
import sys
import pathlib

form_class = uic.loadUiType("updateCheck.ui")[0]  # Load the UI


# TODO
# Find solution for creating EXE and MSI files. (https://cx-freeze.readthedocs.io/en/latest/setup_script.html#bdist-msi)
# Create function to look for updates via Github Releases.
#   - Make sure to have failsafe in case of no internet etc.
#   - Create "No Updates" argument?
# Create function to download new realease, if any.
# Create function to runs MSI file that updates the program.
# Create function that launches the main program.

class MyWindowClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # self.CheckForUpdate()

    def CheckForUpdate(self):

        # https://github.com/USER/PROJECT/releases/latest/download/package.zip
        print()


app = QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
