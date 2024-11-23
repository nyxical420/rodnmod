from platform import system
from os import execv, path, chdir
from subprocess import run, CREATE_NO_WINDOW

chdir(path.dirname(path.abspath(__name__)))

if path.exists("update.zip"):
    if system() == 'Windows':
        command = ['powershell', 'Expand-Archive', "update.zip", '-DestinationPath', '.', '-Force']
    else:
        command = ['unzip', '-o', "update.zip", '-d', '.']

    run(command, check=True, creationflags=CREATE_NO_WINDOW)

execv("./rnmupdater.exe", ["./rnmupdater.exe"])
