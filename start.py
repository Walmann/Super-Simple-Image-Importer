# import CheckUpdate
import os
import win32api
import requests


GithubURL = "https://api.github.com/repos/Walmann/SuperSimpleImageImporter/releases/latest"

def get_github_repo(extraURL=""):
    try:
        response = requests.get(GithubURL+extraURL)
        if response.status_code == 200:
            return response.json()
        raise Exception
            
    except Exception as e:
        print(e)

def get_file_version():
    path= str(os.getcwd())+"\Importer.exe" # BUG Cant find file when using EXE. 
    # path= "build\exe.win-amd64-3.10\Importer.exe"
    info = win32api.GetFileVersionInfo(path, '\\')
    ms = info['FileVersionMS']
    ls = info['FileVersionLS']
    temp = win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls)
    exe_version = "".join(str(x) for x in temp)
    return exe_version

# todo standard ap for heic osv
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
    else: 
        return False


if check_new_version():
    print("New Verion Available")
    

