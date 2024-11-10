import os
from cx_Freeze import setup, Executable

# Function to gather all files in the folder (including subdirectories)
def gather_files(src_folder):
    files = []
    for dirpath, dirnames, filenames in os.walk(src_folder):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            relative_path = os.path.relpath(full_path, src_folder)
            files.append((full_path, relative_path))
    return files

# Gather all files from the 'assets' folder
include_files = gather_files("./assets")

# List of required libraries and explicit includes for cx_Freeze
build_exe_options = {
    "packages": ["httpx", "psutil", "pymsgbox", "rapidfuzz", "rodnmod"],
    "excludes": ["tkinter", "cx_freeze"],  # Exclude unnecessary libraries
    "include_files": include_files,        # Include files in the assets folder
    "includes": ["pywebview"],             # Explicitly include pywebview
}

exe = Executable(
    script="main.py",  # Replace with your main script
    base="Win32GUI",    # Prevent console window from appearing
    target_name="rodnmod.exe"  # Specify the name of the .exe file
)

# Setup configuration
setup(
    name="Rod n' Mod",
    version="1.1.2-alpha",
    description="A webfishing-themed mod manager!",
    options={"build_exe": build_exe_options},
    executables=[exe]
)
