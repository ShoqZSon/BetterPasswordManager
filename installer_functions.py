import validateLocation as VL
import validateUserInput as VU
import utilities as util
import os


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
        :rtype: bool
    """

    if not os.path.exists(location):
        print("Path does not exist")
        return False

    if not os.path.isdir(location):
        print("Path is not a directory")
        return False

    if not os.access(location, os.W_OK):
        print("Path is not writable")
        return False

    if VL.checkSpace(location):
        print("Disk has not enough space left")
        return False

    return True

def validateUserInput() -> str:
    """
        Validates the user input by checking if the input is empty, too long (>200 chars), or contains any forbidden characters.

        :return: The location of the installation as a string.
        :rtype: str
    """

    install_path = input("Please enter the installation path: ")

    if util.inputEmpty(install_path):
        raise ValueError("Input == 0")
    elif len(install_path) > VU.MAX_INPUT_LENGTH:
        raise ValueError("Input too large")

    forbiddenChars = r'<>"|?*!§$&°^`´'
    if VU.invalidChars(install_path, forbiddenChars):
        raise ValueError("Invalid input")

    return install_path