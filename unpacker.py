from os import execv, path
from py7zr import SevenZipFile

if path.exists("update.7z"):
    with SevenZipFile("update.7z", mode='r') as archive:
        archive.extractall(path=".")

execv("./rnmupdater.exe", ["./rnmupdater.exe"])