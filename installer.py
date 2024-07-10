import installer_functions as inst_f
import utilities as util
#TODO include logging
import sys

try:
    # validate the user input
    install_path = inst_f.validateUserInput()

    # validate the given location
    inst_f.validateLocation(install_path)

    # creates the base folder for the application files

    directory = util.createFolder(install_path, "BetterPasswordManager")

    util.createFile(directory, "config.json")
    util.createFile(directory, "key.key")
    util.createFile(directory, "database.txt")
    util.createFile(directory, "usernames.txt")
    util.createFile(directory, "passwords.txt")
except Exception as e:
    print(e)
    sys.exit(1)

