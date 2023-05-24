import win32api
import requests
# import tempfile
from zipfile import ZipFile
import io

import os

GithubURL = "https://api.github.com/repos/Walmann/SuperSimpleImageImporter/releases/latest"




def writeError(e):
    from importer import writeLog
    writeLog(e)


def get_github_repo(extraURL=""):
    try:
        response = requests.get(GithubURL+extraURL)
        if response.status_code == 200:
            return response.json()
        raise Exception
            
    except Exception as e:
        writeError(e=e)

def get_file_version():
    # try: 
        path= str(os.getcwd())+"\Importer.exe" # BUG Cant find file when using EXE. 
        # path= "build\exe.win-amd64-3.10\Importer.exe"
        info = win32api.GetFileVersionInfo(path, '\\')
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        temp = win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls)
        exe_version = "".join(str(x) for x in temp)
        return exe_version
    # except Exception as e:
    #     raise Exception(f"Info: {info}\n {e}")

def get_github_version():
    # response = requests.get(GithubURL)
    # Online_version = response.json()["name"]
    Online_version = get_github_repo()["name"]
    github_version_tuple = tuple(map(int, Online_version[1:].split(".")))
    github_version_tuple = "".join(str(x) for x in github_version_tuple).ljust(4, "0")
    return github_version_tuple



def check_new_version():
    print(get_github_version())
    print(get_file_version())

    if get_github_version() >= get_file_version():
        return True
    else: return False


def download_latest_release():
    import pathlib
    from os import getenv
    # Find latest release Zip:
    for link in get_github_repo()["assets"]:
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




def install_update():
    updateLocation = download_latest_release()


    batUpdater = "./updateFile.bat"

    UpdateLocation= updateLocation
    ProgramLocation= os.getenv("LOCALAPPDATA") + "\\Programs\\Super Simple Image Importer\\"


    # import os
    # import shutil
    # import subprocess


    # # Download the latest zip, extracts to Update folder
    # updateLocation = download_latest_release()

    # programLocation = os.getenv("LOCALAPPDATA") + "\\Programs\\Super Simple Image Importer\\"

    # # Delete the current program, exept settings folder.
    # for filename in os.listdir(programLocation):
    #     file_path = os.path.join(programLocation, filename)
    #     try:
    #         if os.path.isdir(file_path) and file_path.endswith("Settings"): 
    #             pass
    #         elif os.path.isfile(file_path) or os.path.islink(file_path):
    #             os.unlink(file_path)
    #         elif os.path.isdir(file_path):
    #             shutil.rmtree(file_path)
    #     except Exception as e:
    #         print('Failed to delete %s. Reason: %s' % (file_path, e))
    
    
    # try:
    #     shutil.copytree(updateLocation, programLocation, dirs_exist_ok=True)
        
    # except Exception as e:
    #     print("Error: ")
    #     print(e)
    #     writeError(e=e)

    # import sys
    # Restart the program:
    # subprocess.call([programLocation+"Importer.exe"])
    # subprocess.run('"{}"'.format(programLocation+"Importer.exe"))
    # os.system('"{}"'.format(programLocation+"Importer.exe"))
    # sys.exit()