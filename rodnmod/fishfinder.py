from os import path, walk

def findWebfishing():
    """
    Finds the webfishing installation folder.
    """
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
        if path.isfile(location):
            with open(location, 'r') as file:
                steamLibraries.extend(line.split('"')[3] for line in file if '"path"' in line)

    for library in steamLibraries:
        common_path = path.join(library, "steamapps", "common")
        if path.exists(common_path):
            for dirpath, dirnames, _ in walk(common_path):
                if "WEBFISHING" in dirnames:
                    installationPath = path.join(dirpath, "WEBFISHING")
                    if path.isfile(path.join(installationPath, "webfishing.exe")):
                        return installationPath

    return None