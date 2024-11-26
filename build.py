import os
import shutil
import zipfile
import platform
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

systems = {
    "Windows": "win",
    "Linux": "linux"
}

userOS = systems[platform.system()]

items = [
    "version.json",
    "main.html",
    "updater.html",
]

if userOS == "win":
    items.append("winupdate.bat")
    items.append("7zr.exe")
    items.append("rodnmod.exe")
elif userOS == "linux":
    items.append("linuxupdate.sh")
    # 7zip console version for linux
    # rodnmod for linux (i forgot if it even has a binary)

print("Zipping files...")
with zipfile.ZipFile("rodnmod-standalone-" + systems[platform.system()] + ".zip", 'w') as zipf:
    for item in items:
        if os.path.isfile(item):
            zipf.write(item, os.path.basename(item))
            print(f"Added file: {item}")
        elif os.path.isdir(item):
            for root, dirs, files in os.walk(item):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, os.path.dirname(item)))
                    print(f"Added file from directory: {file_path}")
        else:
            print(f"Item {item} does not exist and will be skipped.")

print(f"Build complete.")