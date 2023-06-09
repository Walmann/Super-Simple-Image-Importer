# from ptpy import PTPy

# with PTPy() as camera:
#     # Get the list of storage IDs
#     storage_ids = camera.get_storageids()

#     # Get the list of object handles for the first storage ID
#     object_handles = camera.get_objecthandles(storage_ids[0])

#     # Get the first 10 object handles
#     object_handles = object_handles[:10]

#     # Get the object info for each object handle
#     for handle in object_handles:
#         info = camera.get_objectinfo(handle)
#         print(info.Filename)




import os
import ctypes
import ctypes.util

# NOTE: This code *may* work on windows, I don't have a win32 system to test
# this on. 
_module_path = ctypes.util.find_library("mtp") 
_libmtp = ctypes.CDLL(_module_path)

print()
# import pymtp.pymtp as MTPisSHIT

# # Create an MTP device object
# mtp = MTPisSHIT.MTP()



# devices = mtp.get_devices()
# # # Connect to the first available MTP device
# # mtp.connect()

# # # Get a list of all files and folders on the device
# # files = mtp.get_filelisting()

# # # Print the names of the first 10 files
# # for file in files[:10]:
# #     print(file.filename)

# # Disconnect from the device
# mtp.disconnect()
