import os
import json
from PySide6.QtWidgets import QMessageBox

def createFolder(location: str, folderName: str) -> str:
    """
        Creates a directory at the specified path.

        :param location: The path where the directory should be created.
        :type location: str
        :param folderName: The name of the folder to create.
        :type folderName: str
        :raises FileExistsError: If the folder already exists.
        :return: The created folder on success.
    """

    directory = os.path.join(location, folderName)

    os.makedirs(directory, mode=0o700, exist_ok=True)
    print(f"Directory '{folderName}' created at: {location}")

    return directory

def createFile(location: str, fileName: str) -> bool:
    """
    Creates a file at the specified path.
    :param location: The path where the file should be created.
    :type location: str
    :param fileName: Name of the file to create.
    :type fileName: str
    :returns True if the file was created, False otherwise.
    """

    file = os.path.join(location, fileName)
    if os.path.exists(file):
        raise FileExistsError (f"{file} already exists")

    # writes an empty file
    with open(file, "w") as f:
        f.write('')

    print(f"File '{fileName}' created at: {location}")

    return True

def writeJson(location: str, fileName: str, data) -> bool:
    """Writes data to a JSON file.

    Args:
        location (str): The directory where the JSON file will be saved.
        fileName (str): The name of the JSON file (should end with .json).
        data: The data to write to the JSON file (must be serializable).

    Returns:
        bool: True if the file was written successfully, False otherwise.
    """
    try:
        # Ensure the directory exists
        os.makedirs(location, exist_ok=True)

        # Create the full file path
        file_path = os.path.join(location, fileName)

        # Write the data to the JSON file
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        return True
    except Exception as e:
        print(f"Error writing JSON file: {e}")
        return False



def show_notification(text):
    # Create a QMessageBox
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(text)
    msg_box.setWindowTitle("Error!")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec()