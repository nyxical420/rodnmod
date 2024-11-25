import os
import shutil
import subprocess

buildCommand = [
    'pyinstaller',
    '--onefile',
    '--noconsole',
    '--icon=./assets/rodnmod.ico',
    '--paths=./rodnmod',
    '--strip',

    '--exclude-module=pyinstaller',

    '--add-data=main.html;.',
    '--add-data=assets/scripts/*;assets/scripts',
    '--add-data=assets/web/*;assets/web',
    '--add-data=assets/web/fishing/*;assets/web/fishing',
    '--add-data=assets/web/fishing/sounds/*;assets/web/fishing/sounds',

    '--upx-dir=./upx',

    'main.py'
]

subprocess.run(buildCommand)

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