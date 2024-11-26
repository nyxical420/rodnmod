import os
import shutil
import platform
import subprocess

subprocess.run(["pyarmor", "gen", "main.py"])

systems = {
    "Windows": "win",
    "Linux": "linux"
}

userOS = systems[platform.system()]

# windows
if userOS == "win":
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
        '--add-data=assets/web/*;assets/web',
        '--add-data=assets/web/fishing/*;assets/web/fishing',
        '--add-data=assets/web/fishing/sounds/*;assets/web/fishing/sounds',
        '--add-data=assets/scripts/*;assets/scripts',
        '--upx-dir=./upx',

        'dist/main.py'
    ]

    subprocess.run(buildCommand)

    if os.path.exists('./dist/main.exe'):
        shutil.move('./dist/main.exe', './rodnmod.exe')

# linux
if userOS == "linux":
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

        '--add-data=rodnmod:rodnmod',
        '--add-data=assets/web/*:assets/web',
        '--add-data=assets/web/fishing/*:assets/web/fishing',
        '--add-data=assets/web/fishing/sounds/*:assets/web/fishing/sounds',
        '--add-data=assets/scripts/*:assets/scripts',
        '--upx-dir=./upx',

        'dist/main.py'
    ]

    subprocess.run(buildCommand)

    if os.path.exists('./dist/main'):
        shutil.move('./dist/main', './rodnmod')

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

items = [
    "assets",
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
    items.append("rodnmod")

print("Zipping files with 7z...")

zip_command = [
    "./7zr", "a", 
    "rodnmod-standalone-" + systems[platform.system()] + ".7z",
    "-xr!assets/repository"
]

for item in items:
    if os.path.exists(item):
        zip_command.append(item)
        print(f"Added: {item}")

# Run the 7z command
subprocess.run(zip_command)

print("Build complete.")
