import os
import shutil
import subprocess

subprocess.run(["pyarmor", "gen", "main.py"])

buildCommand = [
    'pyinstaller',
    '--onefile',
    '--noconsole',
    '--icon=./assets/rodnmod.ico',
    '--strip',

    '--hidden-import=httpx',
    '--hidden-import=semver',
    '--hidden-import=psutil',
    '--hidden-import=webview',
    '--hidden-import=rapidfuzz',
    '--hidden-import=pyperclip',

    '--exclude-module=_distutils_hack',
    '--exclude-module=tkinter',
    '--exclude-module=xmlrpc',
    '--exclude-module=anyio',
    '--exclude-module=asyncio',
    '--exclude-module=autocommand',
    '--exclude-module=curses',
    '--exclude-module=jaraco',
    '--exclude-module=lib2to3',
    '--exclude-module=pip',
    '--exclude-module=pyinstaller',
    '--exclude-module=pyarmor',

    '--add-data=rodnmod;rodnmod',
    '--upx-dir=./upx',

    'dist/main.py'
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