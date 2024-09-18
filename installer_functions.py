import validateLocation as VL
import validateUserInput as VU
import baseFolder as bF
import utilities as util
import os


def validateUserInput() -> str:
    """
        Validates the user input by checking if the input is empty, too long (>200 chars), or contains any forbidden characters.

        :return: The location of the installation as a string.
        :return: str
    """

    install_path = input("Please enter the absolute installation path: ")

    if util.inputEmpty(install_path):
        raise ValueError("Input == 0")
    elif len(install_path) > VU.MAX_INPUT_LENGTH:
        raise ValueError("Input too large")

    forbiddenChars = r'<>"|?*!§$&°^`´'
    if VU.invalidChars(install_path, forbiddenChars):
        raise ValueError("Invalid input")

    return install_path

def validateLocation(location: str) -> bool:
    """
        Validates the given location with the following checks:
            - Does the given path exist?
            - Is the path a directory?
            - Does the user have permission to access the directory?
            - Does the disk have enough space (at least 50MB)?

        :param location: The location where the application is supposed to be installed.
        :type location: str
        :return: True if every check is successful, False otherwise.
    """

    if not os.path.exists(location):
        raise ValueError("Path does not exist")

    if not os.path.isdir(location):
        raise ValueError("Path is not a directory")

    # checks if the path is writable for the user
    if not os.access(location, os.W_OK):
        raise ValueError("Path is not writable")

    if VL.checkSpace(location):
        raise ValueError("Disk has not enough space left")

    return True

