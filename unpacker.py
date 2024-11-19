import platform
import subprocess
from os import execv

if platform.system() == 'Windows':
    command = ['powershell', 'Expand-Archive', "update.zip", '-DestinationPath', '.', '-Force']
else:
    command = ['unzip', '-o', "update.zip", '-d', '.']

subprocess.run(command, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
execv("./rnmupdater.exe", ["./rnmupdater.exe"])
