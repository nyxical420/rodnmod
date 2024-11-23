import os
from json import load
from sys import platform
from cx_Freeze import setup, Executable
import subprocess

# Function to obfuscate code with PyArmor 8
def obfuscate_code():
    # List of scripts to obfuscate
    scripts_to_obfuscate = ['main.py', 'updater.py', 'unpacker.py']
    
    for script in scripts_to_obfuscate:
        # Generate an obfuscated version using pyarmor gen
        subprocess.run(["pyarmor", "gen", script])

# Call the obfuscation function before building
obfuscate_code()

# Read the `version.json` file for version information
with open("version.json") as ver:
    version = load(ver)["version"]

# List of files to include in the build
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
]

# Configure the `cx_Freeze` build
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
                "pythonnet",  # Needed in your environment
            ]
        }
    },
    executables=[
        Executable(
            "dist/main.py",  # Pointing to the obfuscated script
            icon="./assets/rodnmod.ico",
            base=("Win32GUI" if platform == "win32" else None),
            target_name="rodnmod"
        ),
        Executable(
            "dist/updater.py",  # Pointing to the obfuscated script
            icon="./assets/updater.ico",
            base=("Win32GUI" if platform == "win32" else None),
            target_name="rnmupdater"
        ),
        Executable(
            "dist/unpacker.py",  # Pointing to the obfuscated script
            icon="./assets/unpacker.ico",
            base=("Win32GUI" if platform == "win32" else None),
            target_name="rnmunpacker"
        )
    ],
)
