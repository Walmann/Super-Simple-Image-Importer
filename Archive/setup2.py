

# Create setup EXE for the program. THIS IS THAT EXE FILE!!!!!
# This file shall install the program to a directory. For updating I'm creating another script.
# To make this as easy as possible, you can't select where to install the program.

# I need to pack this file together with the install files into a single EXE file.


#order of bussiness:
# Check for admin rights (Check if that is needed att all)
#   # If not, restart with admin rights. 
# Check if dir_root is available.
#   # if not, create it.
# put all the files inside dir_root folder.
# Create a desktop shortcut.
# create a start meny shortcut.
# Start the program

import ctypes
import shutil
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except: 
        return False

# Check for admin
if not is_admin():
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


# Check for install dir:
dir_root = os.path.join(os.environ['APPDATA'], 'walmann', 'SSII')
dir_install = os.path.join(dir_root, 'app')
dir_settings = os.path.join(dir_root, 'settings')


#Check if folders exist
    # If they do, delete install folder
    # If NOT, create them.
if not os.path.exists(dir_root):
    os.mkdir(dir_root)
if os.path(dir_install).is_dir():
    shutil.rmtree(dir_install)


# Now we create all the needed folders inside the root folder:
os.mkdir(dir_install)
os.mkdir(dir_settings)


