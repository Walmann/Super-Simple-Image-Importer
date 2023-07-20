import sys
# from bin.debug_write import isDebug
# if isDebug:
def isDebug():
    nameSplit1 = sys.argv[0].split("/")[-1] 
    nameSplit2 = sys.argv[0].split("\\")[-1] 

    debugExeNames = ["app.py", "SSII_CLI.exe"]

    if nameSplit1 in debugExeNames or nameSplit2 in debugExeNames:
        return True
    else: 
        return False


def returnName():
        # name = sys.argv[0].split("/")[-1] 
        nameSplit2 = sys.argv[0].split("\\")[-1] 
        return str(f"{nameSplit2} isDebug: {isDebug()}")