import os
import shutil
import subprocess

pyinstaller_command = [
    'pyinstaller',
    '--onefile',
    '--noconsole',
    '--icon=./assets/rodnmod.ico',
    '--paths=./rodnmod',
    'main.py'
]

subprocess.run(pyinstaller_command)

if os.path.exists('./dist/main.exe'):
    shutil.move('./dist/main.exe', './rodnmod.exe')

remove = [
    "./build",
    "./dist",
    "./main.spec",
]

for item in remove:
    if os.path.exists(item):
        if os.path.isdir(item):
            shutil.rmtree(item)
        else:
            os.remove(item)

print(f"Build complete.")
