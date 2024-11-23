from os import execv, path
from py7zr import SevenZipFile

with SevenZipFile("update.7z", mode='r') as archive:
    for file in archive.getnames():
        try:
            archive.extract(path=".", targets=[file])
        except Exception as e:
            print(f"Skipping {file} due to error: {e}")

input("continue")

execv("./rnmupdater.exe", ["./rnmupdater.exe"])