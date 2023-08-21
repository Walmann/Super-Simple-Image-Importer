import sys
import win32con as wcon
import win32api
import win32file


def fetch_devices():
    found_devices = {}

    
    # Find all removable drives
    # drive_types=(wcon.DRIVE_REMOVABLE, wcon.DRIVE_CDROM) #FUTURE CD/DVD Support?
    drive_types=(wcon.DRIVE_REMOVABLE,)
    drives_str = win32api.GetLogicalDriveStrings()
    drives = (item for item in drives_str.split("\x00") if item)

    drive_letter_list = []

    for item in drives:
        if not drive_types or win32file.GetDriveType(item) in drive_types:
            drive_letter_list.append(item)


    # Add drives to found_devices
    for drive in drive_letter_list:
        # Get drive name
        drive_info = win32api.GetVolumeInformation(f"{drive}")

        found_devices[drive] = {
            "device_name": drive_info[0],
            # "device_subname": device_subname,
            "device_id": drive,
            "device_path": drive,
            "device_path_pretty": drive[:2]
        }
    
    
    return found_devices
    print()
    

    # def get_drives_list(drive_types=(wcon.DRIVE_REMOVABLE,)):
    #     drives_str = win32api.GetLogicalDriveStrings()
    #     drives = (item for item in drives_str.split("\x00") if item)
    #     return [
    #         item[:2]
    #         for item in drives
    #         if not drive_types or win32file.GetDriveType(item) in drive_types
    #     ]

    # drive_filters_examples = (
    #     (None, "All"),
    #     ((wcon.DRIVE_REMOVABLE,), "Removable"),
    #     ((wcon.DRIVE_FIXED, wcon.DRIVE_CDROM), "Fixed and CDROM"),
    # )
    # for drive_types_tuple, display_text in drive_filters_examples:
    #     drives = get_drives_list(drive_types=drive_types_tuple)
    #     # print(f"{display_text} drives:")
    #     for drive in drives:
    #         driveInfo = win32api.GetVolumeInformation(f"{drive}\\")
    #     #     print(f"{drive }{drive2}", end="")

    #         # Put into dict that gets returned.
    #         found_devices[device_id] = {
    #             "device_name": device_name,
    #             # "device_subname": device_subname,
    #             "device_path": device_path
    #         }
