import platform

MAX_INPUT_LENGTH = 500

def invalidChars(inputString: str, forbiddenChars: list) -> bool:
    """
        Checks if there are any forbidden characters inside the given string.

        :param inputString: The string to check.
        :type inputString: str
        :param forbiddenChars: A string of characters that are forbidden.
        :type forbiddenChars: str
        :return: True if there are any forbidden characters, False otherwise.
        :rtype: bool
    """

    return any(char in forbiddenChars for char in inputString)

def getOS() -> str:
    """
        Returns the operating system of the current system.

        :return: The name of the operating system.
        :rtype: str
    """

    return platform.system()
