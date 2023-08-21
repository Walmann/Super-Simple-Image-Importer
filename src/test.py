



# import mtpy



# temp = mtpy.get_raw_devices()


# print()




import pymtp

devices = pymtp.get_devices()
device = devices[0]  # Assume only one device is connected
# Connect to the device
with pymtp.MTPDevice(device.device_entry) as mtp:
    # List the directories on the device
    dirs = mtp.get_folder_list()
    
print()

