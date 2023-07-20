import subprocess
import re

# import os
from bin.debug_write import isDebug


def unmount_MTP_device(device=None, unmount_all=True, unmount_all_debug=False):
    if unmount_all_debug is True:
        unmount_all = False
    if unmount_all:
        try:
            # subprocess.check_output(["taskkill", "/F", "/IM", "mtpmount-x64.exe"])
            subprocess.Popen(
                ["taskkill", "/F", "/IM", "mtpmount-x64.exe"],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except subprocess.CalledProcessError:
            pass
        # device = fetch_devices()
    if unmount_all_debug:
        try:
            subprocess.Popen(
                ["taskkill", "/F", "/IM", "mtpmount-x64.exe"],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
            )
        except subprocess.CalledProcessError:
            pass


def mount_MTP_device(device, debug=False):
    """Mounts MTP device from the "device" arg

    Args:
        device (dict): dict containing device information for the device that shall be mounted

    Returns:
        dict: Returns information about the path to the newly mounted device.
    """

    # Mount the device
    proc = subprocess.run(
        ["./bin/mtpmount-x64.exe", "mount", f"#{device['device_id']}"],
        stdout=subprocess.PIPE,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    try:
        Output = proc.stdout.decode()
    except AttributeError as e:
        if isDebug():
            print(e)
        else: 
            pass

    if isDebug():
        print(f"Mounting MTP Device Output: \n{Output}")

    # Get info from Output of command above
    re_pattern_drive_letter_name = "((Drive )(.).*? is now (.*?). Don't)"
    info = re.findall(re_pattern_drive_letter_name, Output)
    drive_letter = info[0][2]
    drive_name = info[0][3].split("\\")[-1]
    mount_info = {
        "drive_letter": drive_letter,
        "drive_name": drive_name,
        "drive_path": f"{drive_letter}://",
    }

    return mount_info


def fetch_devices():
    """Fetch USB devices using the MTP protocol.

    Returns:
        dict: USB devices found.
    """
    re_pattern = "(Connection .*?:).*?(\|--.*?\])"
    # re_pattern = "\|--.*?\]"
    proc = subprocess.Popen(
        ["./bin/mtpmount-x64.exe", "list", "available"], stdout=subprocess.PIPE,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    try:
        # Output = proc.stdout.decode()
        Output = str(proc.stdout.read())
    except AttributeError as e:
        if isDebug():
            print(e)
        else: 
            pass
    found_devices_raw = re.findall(re_pattern, Output, re.DOTALL)

    found_devices = {}
    # re_pattern_splitter = "(\|--)(.* )(\[.*\])"
    for devices in found_devices_raw:
        # Get device ID
        re_pattern_device_id = "(\[ID #)(.*?)(\])"
        device_id = re.findall(re_pattern_device_id, devices[1])[0][1]

        # Get name of device
        device_name = devices[0].replace("Connection ", "")[:-1]

        # Get deive Subname. "Storage Intern Lagring" etc.
        re_pattern_subname = "(\|--)(.*?)(\[)"
        device_subname = re.findall(re_pattern_subname, devices[1])[0][1].strip()

        # Put into dict that gets returned.
        found_devices[device_id] = {
            "device_name": device_name,
            "device_id": device_id,
            "device_subname": device_subname,
        }

    return found_devices
