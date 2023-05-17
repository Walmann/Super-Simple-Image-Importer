import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar, QLabel, QDesktopWidget
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from os import getenv, listdir, path, unlink, walk, makedirs
from shutil import rmtree, copy, copytree
import requests



GithubURL = "https://api.github.com/repos/Walmann/SuperSimpleImageImporter/releases/latest"
InstallLocation = getenv("LOCALAPPDATA")+"\\Programs\\Super Simple Image Importer\\"

class InstallerThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()


    def run(self):
        for i in range(101):
            self.progress_signal.emit(i)
            self.msleep(50)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Super Simple Image Importer Installer'
        self.width = 400
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icon.png'))

        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(int((screen.width()-self.width)/2), int((screen.height()-self.height)/2), self.width, self.height)

        self.installButton = QPushButton('Installer Super Simple Image Importer', self)
        self.installButton.setToolTip('Klikk for å installere Super Simple Image Importer')
        self.installButton.resize(300,50)
        self.installButton.move(50,50)
        self.installButton.clicked.connect(self.installClicked)

        self.progressLabel = QLabel('', self)
        self.progressLabel.move(50, 110)

        # self.progressBar = QProgressBar(self)
        # self.progressBar.setGeometry(50, 140, 300, 25)
        # self.progressBar.setValue(0)

        self.show()

    def installClicked(self):
        self.installButton.setEnabled(False)
        self.installerThread = InstallerThread()
        self.installerThread.progress_signal.connect(self.installProgram)
        self.installerThread.start()

    def installProgram(self, progress):
        updateLocation = download_latest_release(self)
        # totalFiles = count_files(updateLocation)
        # self.progressBar.setMaximum(totalFiles)


        
        # Delete the current program, exept settings folder, it if exists
        # TODO Create proper update, with progressbar.

        self.progressLabel = QLabel('Sletter gammel kopi', self)
        if path.isdir(InstallLocation):
            backupLoc = getenv("TEMP")+"\\SSIIbackup"
            copy(InstallLocation+"Settings", backupLoc)
            rmtree(InstallLocation)

        # if path.isdir(InstallLocation):
        #     for filename in listdir(InstallLocation):
        #         file_path = path.join(InstallLocation, filename)
        #         try:
        #             if path.isdir(file_path) and file_path.endswith("Settings"): 
        #                 pass
        #             elif path.isfile(file_path) or path.islink(file_path):
        #                 unlink(file_path)
        #             elif path.isdir(file_path):
        #                 rmtree(file_path)
        #             self.progressBar.setValue(self.progressBar.value() + 1)
        #         except Exception as e:
        #             print('Failed to delete %s. Reason: %s' % (file_path, e))



        # Install program: 
        self.progressLabel = QLabel('Kopierer ny versjon', self)
        copytree(updateLocation, InstallLocation)
        copy(backupLoc, InstallLocation+"Settings\\")
        # TODO Create a progressbar for copying the files. 
        # for root, dirs, files in walk(updateLocation):
        #     for file in files:
        #         src_path = path.join(root, file)
        #         temp = path.relpath(src_path, file)
        #         dst_path = path.join(InstallLocation, path.relpath(src_path, file))
        #         copy(src_path, dst_path)
        #         self.progressBar.setValue(self.progressBar.value() + 1)
        #     for dir in dirs:
        #         src_path = path.join(root, dir)
        #         dst_path = path.join(InstallLocation, path.relpath(src_path, file))
        #         if not path.exists(dst_path):
        #             makedirs(dst_path)
        #         self.progressBar.setValue(self.progressBar.value() + 1)
        print()


def count_files(path):
    num_files = 0
    for root, dirs, files in walk(path):
        num_files += len(files)
    return num_files

def get_github_repo(self, extraURL=""):
    try:
        response = requests.get(GithubURL+extraURL)
        if response.status_code == 200:
            return response.json()
        raise Exception
            
    except Exception as e:
        print(e)

def download_latest_release(self):
    import pathlib
    from os import getenv
    # Find latest release Zip:
    for link in get_github_repo(self)["assets"]:
        if link["name"].lower().endswith(".zip"):
            newestZip = link["browser_download_url"]
            break


    UpdateFile = getenv("TEMP")+"\\ImageImporterUpdate\\"
    return pathlib.Path(UpdateFile).absolute() # DEBUGLINE This line just make it not download the update every single time :) 
    # Download and extract the latest Zip file:
    r = requests.get(newestZip)
    z = ZipFile(io.BytesIO(r.content))
    z.extractall(UpdateFile)

    return pathlib.Path(UpdateFile).absolute()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
