import requests
import tempfile
import subprocess
from urllib.parse import urlparse
import sys
import os
from PySide6.QtWidgets import QApplication, QMessageBox
from bin.debug_write import isDebug, writeDebug


def update_prompt(local_ver, remote_ver):
    msg = QMessageBox()
    msg.setWindowTitle("Oppdatering")
    msg.setText(f"Det finnes en ny oppdatering til programmet.<br>Vil du laste ned og installere oppdateringen?<br><br>Din version: {local_ver}<br>Ny version: {remote_ver}")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    result = msg.exec_()
    if result == QMessageBox.Yes:
        return True
    else:
        return False



def download_and_install_latest_release(local_ver, remote_ver):
    if update_prompt(local_ver, remote_ver):
        repo_url = 'https://github.com/Walmann/SuperSimpleImageImporter'
        
        # Get the temporary folder path using the %temp% environment variable
        tmpdir = os.path.join(os.environ['TEMP'], 'SuperSimpleImageImporter')
        os.makedirs(tmpdir, exist_ok=True)

        api_url = repo_url.replace('github.com', 'api.github.com/repos') + '/releases/latest'
        response = requests.get(api_url)
        data = response.json()
        download_url = data['assets'][0]['browser_download_url']
        filename = urlparse(download_url).path.split('/')[-1]
        response = requests.get(download_url)
        file_path = os.path.join(tmpdir, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        writeDebug(f'Lastet ned {filename} til {tmpdir}')
        subprocess.Popen([file_path])
        sys.exit()
