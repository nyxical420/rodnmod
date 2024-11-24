import subprocess
from json import load
from sys import platform
from cx_Freeze import setup, Executable

# PyArmor layer to obfuscate scripts - hopefully lowers AV detection
for script in ['main.py', 'updater.py']:
    subprocess.run(["pyarmor", "gen", script])

with open("version.json") as ver:
    version = load(ver)["version"]

# Build Rod n' Mod with required stuff
include_files = [
    ('LICENSE', 'LICENSE'),
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

    ('dist/pyarmor_runtime_000000', 'lib/pyarmor_runtime_000000'),
    ('rodnmod', 'lib/rodnmod'),

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
            "dist/main.py",
            icon="./assets/rodnmod.ico",
            base=("Win32GUI" if platform == "win32" else None),
            target_name="rodnmod"
        ),
        Executable(
            "dist/updater.py",
            icon="./assets/rodnmod.ico",
            base=("Win32GUI" if platform == "win32" else None),
            target_name="rnmupdater"
        )
    ],
)
