import sys
# from bin.debug_write import isDebug
# if isDebug:
def isDebug():

   

    name = sys.argv[0].split("/")[-1] 
    if name == "app.py" or name == "SSII_CLI.exe": # TODO NEXT Popup vinduer i EXE filen. Finn ut hvorfor.
        return True
    else: 
        return False


def returnName():
        name = sys.argv[0].split("/")[-1] 
        return str(name)