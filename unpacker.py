from os import execv
from platform import system
from subprocess import run, CREATE_NO_WINDOW

if system() == 'Windows':
    command = ['powershell', 'Expand-Archive', "update.zip", '-DestinationPath', '.', '-Force']
else:
    command = ['unzip', '-o', "update.zip", '-d', '.']

run(command, check=True, creationflags=CREATE_NO_WINDOW)
execv("./rnmupdater.exe", ["./rnmupdater.exe"])
