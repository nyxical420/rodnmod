import psutil
import logging
import platform
from os import path, walk

logging.basicConfig(
    filename='rodnmod.log',
    level=logging.INFO,
    format="%(asctime)s - rodnmod:fishfinder %(levelname)s:  %(message)s"
)

def findWebfishing():
    """
    Finds the webfishing installation folder.
    """
    logging.info("Starting the Webfishing installation search...")

    libraryLocations = [
        # Windows
        path.expandvars(r'%ProgramFiles(x86)%\Steam\steamapps\libraryfolders.vdf'),
        path.expandvars(r'%ProgramFiles%\Steam\steamapps\libraryfolders.vdf'),
        path.expandvars(r'%UserProfile%\Documents\My Games\Steam\libraryfolders.vdf'),
        path.expandvars(r'%ProgramData%\Steam\libraryfolders.vdf'),

        # Linux
        path.expanduser(r'~/.steam/steam/steamapps/libraryfolders.vdf'),
        path.expanduser(r'~/.local/share/Steam/steamapps/libraryfolders.vdf'),
    ]

    steamLibraries = []
    for location in libraryLocations:
        logging.debug(f"Checking library location: {location}")
        if path.isfile(location):
            with open(location, 'r') as file:
                libraries = [line.split('"')[3] for line in file if '"path"' in line]
                steamLibraries.extend(libraries)
                logging.info(f"Found libraries: {libraries}")

    if not steamLibraries:
        logging.info("No predefined libraries found, starting a broader search...")
        if platform.system() == 'Windows':
            drives = []
            for partition in psutil.disk_partitions():
                if 'removable' not in partition.opts:
                    drives.append(partition.mountpoint)
            logging.debug(f"Non-removable drives found: {drives}")
        else:
            drives = ['/']
            logging.debug("Searching in the root directory on Linux")

        for drive in drives:
            logging.debug(f"Searching in drive: {drive}")
            for root, dirs, _ in walk(drive):
                if 'steamapps' in dirs:
                    steamLibraries.append(root)
                    logging.info(f"Found steamapps in: {root}")

    for library in steamLibraries:
        common_path = path.join(library, "steamapps", "common")
        if path.exists(common_path):
            for dirpath, dirnames, _ in walk(common_path):
                if "WEBFISHING" in dirnames:
                    installationPath = path.join(dirpath, "WEBFISHING")
                    logging.info(f"Webfishing found at: {installationPath}")
                    return installationPath

    logging.warning("Webfishing installation not found.")
    return None