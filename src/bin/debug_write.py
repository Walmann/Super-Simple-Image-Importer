import sys


# from bin.debug_write import isDebug
# if isDebug:
def isDebug():
    """Check if the program is launced in CLI mode or not.

    Returns:
        Bool: True = Currently in CLI / Debug mode, False = GUI mode.
    """
    nameSplit1 = sys.argv[0].split("/")[-1]
    nameSplit2 = sys.argv[0].split("\\")[-1]

    debugExeNames = ["app.py", "SSII_CLI.exe"]

    if nameSplit1 in debugExeNames or nameSplit2 in debugExeNames:
        return True
    else:
        return False


def writeDebug(inputText: str):
    """If the CLI version of the program is launched, this function is used to write debug messages to the console. This is due to rapid CMD blinking if the debug messages are being written wile in "No CMD" mode.

    Args:
        inputText (str): _description_
    Returns:
        Bool: Returns True if the debug message was written. Returns False if not writter, usually because the program is not in debug mode.
    """
    if isDebug():
        print(inputText)
        return True
    else:
        return False


def returnName():
    # name = sys.argv[0].split("/")[-1]
    nameSplit2 = sys.argv[0].split("\\")[-1]
    return str(f"{nameSplit2} isDebug: {isDebug()}")
