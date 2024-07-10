import os
import shutil
import platform

MAX_INPUT_LENGTH = 500

"""
Checks if input is empty
:arg 
inputString (str): Path of the location where the application is supposed to be installed
:returns 
bool: True if input is empty, False otherwise
"""
def inputEmpty(inputString: str) -> bool:
    return len(inputString) == 0

"""
"""
def invalidChars(inputString: str, forbiddenChars: str) -> bool:
    return any(char in forbiddenChars for char in inputString)

"""
"""
def getOS() -> str:
    return platform.system()

"""
"""
# check for 50mb of available space
def checkSpace(location: str) -> bool:
    required_space = 50 * 1024 * 1024

    try:
        total, used, free = shutil.disk_usage(location)
        return free < required_space
    except OSError as e:
        print(f"Error checking space at {location}: {e}")
        return False

"""
Validates the user input by checking if the input was empty, too long (>200 chars) or if there were any forbidden characters used.

:returns the location of the installation as a string
"""
def validateUserInput() -> str:
    install_path = input("Please enter the installation path: ")

    if inputEmpty(install_path):
        raise ValueError("Input == 0")
    elif len(install_path) > MAX_INPUT_LENGTH:
        raise ValueError("Input too large")

    forbiddenChars = r'<>"|?*!§$&°^`´'
    if invalidChars(install_path, forbiddenChars):
        raise ValueError("Invalid input")

    return install_path

def validateLocation(location: str) -> bool:
    if not os.path.exists(location):
        print("Path does not exist")
        return False

    if not os.path.isdir(location):
        print("Path is not a directory")
        return False

    if not os.access(location, os.W_OK):
        print("Path is not writable")
        return False

    if checkSpace(location):
        print("Disk has not enough space left")
        return False

    return True
