import shutil

def checkSpace(location: str) -> bool:
    """
        Checks if the disk at the given location has at least 50MB of free space.

        :param location: The path where the application is supposed to be installed.
        :type location: str
        :return: True if there is enough space, False otherwise.
        :rtype: bool
    """

    required_space = 50 * 1024 * 1024 # 50 mb

    try:
        total, used, free = shutil.disk_usage(location)
        return free < required_space
    except OSError as e:
        print(f"Error checking space at {location}: {e}")
        return False
    except Exception as e:
        print(f"Unknown Error: {e}")
        return False
