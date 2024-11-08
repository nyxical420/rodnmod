import os

def findWebfishing():
    """
    Finds the webfishing installation folder.
    """
    libraryLocations = [
        os.path.expandvars(r'%ProgramFiles(x86)%\Steam\steamapps\libraryfolders.vdf'),
        os.path.expandvars(r'%ProgramFiles%\Steam\steamapps\libraryfolders.vdf'),
        os.path.expandvars(r'%UserProfile%\Documents\My Games\Steam\libraryfolders.vdf'),
        os.path.expandvars(r'%ProgramData%\Steam\libraryfolders.vdf'),
    ]

    steamLibraries = []
    for location in libraryLocations:
        if os.path.isfile(location):
            with open(location, 'r') as file:
                steamLibraries.extend(line.split('"')[3] for line in file if '"path"' in line)

    for library in steamLibraries:
        common_path = os.path.join(library, "steamapps", "common")
        if os.path.exists(common_path):
            for dirpath, dirnames, _ in os.walk(common_path):
                if "WEBFISHING" in dirnames:
                    installationPath = os.path.join(dirpath, "WEBFISHING")
                    if os.path.isfile(os.path.join(installationPath, "webfishing.exe")):
                        return installationPath

    return None