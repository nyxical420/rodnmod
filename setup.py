import sys
from json import load
from cx_Freeze import setup, Executable

with open("version.json") as ver:
    version = load(ver)["version"]

include_files = [
    ('main.html', 'main.html'),
    ('updater.html', 'updater.html'),
    ('version.json', 'version.json'),
    ('data/', 'data/'),
    ('data/modpacks', 'data/modpacks'),
    ('data/savefiles', 'data/savefiles'),
    ('assets/scripts', 'assets/scripts'),
    ('assets/web', 'assets/web'),
    ('assets/web/fishing', 'assets/web/fishing'),
    ('assets/web/fishing/sounds', 'assets/web/fishing/sounds'),
]

setup(
    name="Rod n' Mod",
    version=version,
    description="Rod n' Mod",
    options={
        "build_exe": {
            "include_files": include_files,
            "packages": [
                "httpx",
                "psutil",
                "webview",
                "rapidfuzz",
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
                "email"
            ]
        }
    },
    executables=[
        Executable(
            "main.py",
            icon="./assets/rodnmod.ico",
            base=("Win32GUI" if sys.platform == "win32" else None),
            target_name="rodnmod"
        ),
        Executable(
            "updater.py",
            icon="./assets/updater.ico",
            base=("Win32GUI" if sys.platform == "win32" else None),
            target_name="rnmupdater"
        ),
        Executable(
            "unpacker.py",
            icon="./assets/unpacker.ico",
            base=("Win32GUI" if sys.platform == "win32" else None),
            target_name="rnmunpacker"
        )
    ],
)
