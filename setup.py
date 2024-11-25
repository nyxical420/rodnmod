from json import load
from sys import platform
from cx_Freeze import setup, Executable

with open("version.json") as ver:
    version = load(ver)["version"]

# Build Rod n' Mod with required stuff
include_files = [
    ('LICENSE', 'LICENSE'),
    ('main.html', 'main.html'),
    ('updater.html', 'updater.html'),
    ('version.json', 'version.json'),
    ('assets/scripts', 'assets/scripts'),
    ('assets/web', 'assets/web'),
    ('assets/web/fishing', 'assets/web/fishing'),
    ('assets/web/fishing/sounds', 'assets/web/fishing/sounds'),

    ('winupdate.bat', 'winupdate.bat'),
    ('7zr.exe', '7zr.exe'),
]

setup(
    name="Rod n' Mod",
    version=version,
    options={
        "build_exe": {
            "include_files": include_files,
            "packages": [
                "httpx",
                "semver",
                "psutil",
                "webview",
                "rapidfuzz",
                "pyperclip",
                "pythonnet",
            ],
            "excludes": [ # why
                "_distutils_hack",
                "tkinter",
                "zipp",
                "xml",
                "xmlrpc",
                "anyio",
                "asyncio",
                "autocommand",
                "backports",
                "curses",
                "email",
                "jaraco",
                "lib2to3",
                "pip",
                "more_itertools",
                "pyarmor",
            ]
        }
    },
    executables=[
        Executable(
            "main.py",
            icon="./assets/rodnmod.ico",
            base=("Win32GUI" if platform == "win32" else None),
            target_name="rodnmod"
        ),
        Executable(
            "updater.py",
            icon="./assets/rodnmod.ico",
            base=("Win32GUI" if platform == "win32" else None),
            target_name="rnmupdater"
        )
    ],
)
