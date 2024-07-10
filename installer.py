import installer_functions as inst_f
import sys

try:
    install_path = inst_f.validateUserInput()
    print(install_path)
except Exception as e:
    print(e)
    sys.exit(1)

try:
    inst_f.validateLocation(install_path)
except Exception as e:
    print(e)
    sys.exit(1)