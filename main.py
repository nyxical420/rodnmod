# powered by hopes and dreams

import os
import sys
import shutil
import pymsgbox
from json import load
from rapidfuzz import fuzz
from threading import Thread
from difflib import get_close_matches
from webbrowser import open as openWeb
from re import IGNORECASE, compile as comp
from psutil import process_iter, NoSuchProcess
from webview import create_window, start, windows as webWindows

from rodnmod.fishfinder import findWebfishing
from rodnmod.thunderstore import getMods, download, downloadRaw

webfishingInstalled = False
installationPath = findWebfishing()

# thank god stackoverflow my beloved
# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/7675014#7675014
def resource(relative):
    return os.path.join(
        os.environ.get(
            "_MEIPASS2",
            os.path.abspath(".")
        ),
        relative
    )

if installationPath:
    print(f"Installation Path: {installationPath}")
    webfishingInstalled = True
else:
    print("WEBFISHING Installation Path Not Found")

class RodNMod:
    modsList = getMods()
    modsBeingDownloaded = []

    def isInstalled(self):
        return {"installationStatus": webfishingInstalled}
    
    def dragWindow(self, dx, dy):
        window = webWindows[0]
        window.move(window.x + dx, window.y + dy)
    
    def visitSite(self, site: str):
        openWeb(site)

    def launchWebfishing(self, vanilla: bool = False):
        if vanilla:
            try: os.rename(installationPath + "\\GDWeave\\mods", installationPath + "\\GDWeave\\disabled.mods")
            except FileNotFoundError: pass
            self.visitSite("steam://rungameid/3146520")
        else: # modded
            try: os.rename(installationPath + "\\GDWeave\\disabled.mods", installationPath + "\\GDWeave\\mods")
            except FileNotFoundError: pass
            self.visitSite("steam://rungameid/3146520")

    def webfishingInstallation(self):
        return installationPath
    
    def minimizeApplication(self):
        window.minimize()

    def closeApplication(self):
        window.destroy()

    def webfishingRunning(self):
        try:
            if any(process.name() == "webfishing.exe" for process in process_iter()):
                return {"running": True}
            else: 
                return {"running": False}
        except NoSuchProcess:
            return {"running": False}
    
    def say(self, text):
        print(text)
        
    def getModList(self):
        return self.modsList
    
    def refreshModList(self):
        self.modsList = getMods()
        return self.modsList

    def updatedAgo(self, updatedAgo: str):
        time_pattern = comp(r'(\d+)\s*(minutes?|hours?|days?)\s*ago', IGNORECASE)
        match = time_pattern.search(updatedAgo)
        
        if match:
            value = int(match.group(1))
            unit = match.group(2).lower()
        
            if 'minute' in unit:
                return value
            elif 'hour' in unit:
                return value * 60
            elif 'day' in unit:
                return value * 1440
        return 0
        
    
    def searchModList(self, searchQuery: str, filter: str, modTag: str, nsfw: bool):
        if not searchQuery.strip():
            searchQuery = ""

        searchQuery = searchQuery.lower()
        searchResults = {}

        if searchQuery:
            for mod_id, mod_data in self.modsList.items():
                mod_name = mod_data["modName"].lower()
                score = fuzz.WRatio(searchQuery, mod_name)

                if score >= 75:
                    mod_data["fuzz_score"] = score
                    searchResults[mod_id] = mod_data

            searchResults = dict(sorted(searchResults.items(), key=lambda x: x[1]["fuzz_score"], reverse=True))

        else:
            searchResults = self.modsList.copy()

        if not nsfw:
            searchResults = {
                mod_id: mod for mod_id, mod in searchResults.items() if not mod.get("isNSFW", False)
            }

        if filter != "none":
            if filter == "installed":
                ...
            elif filter == "likesCount":
                searchResults = dict(sorted(searchResults.items(), key=lambda x: x[1].get("modScore", 0), reverse=True))
            elif filter == "downloadCount":
                searchResults = dict(sorted(searchResults.items(), key=lambda x: x[1].get("totalDownloads", 0), reverse=True))
            elif filter == "nameA-Z":
                searchResults = dict(sorted(searchResults.items(), key=lambda x: x[1]["modName"].lower()))
            elif filter == "nameZ-A":
                searchResults = dict(sorted(searchResults.items(), key=lambda x: x[1]["modName"].lower(), reverse=True))
            elif filter == "mostDownloaded":
                searchResults = dict(sorted(searchResults.items(), key=lambda x: x[1].get("totalDownloads", 0), reverse=True))
            elif filter == "leastDownloaded":
                searchResults = dict(sorted(searchResults.items(), key=lambda x: x[1].get("totalDownloads", 0)))
            elif filter == "mostLiked":
                searchResults = dict(sorted(searchResults.items(), key=lambda x: x[1].get("modScore", 0), reverse=True))
            elif filter == "leastLiked":
                searchResults = dict(sorted(searchResults.items(), key=lambda x: x[1].get("modScore", 0)))
            elif filter == "newlyUpdated":
                searchResults = dict(sorted(searchResults.items(), key=lambda x: self.updatedAgo(x[1].get("updatedAgo", ""))))
            elif filter == "leastUpdated":
                searchResults = dict(sorted(searchResults.items(), key=lambda x: self.updatedAgo(x[1].get("updatedAgo", "")), reverse=True))
            elif filter.startswith("category:"):
                filter_tags = filter[len("category:"):].strip().lower().split(",")
                searchResults = {
                    mod_id: mod for mod_id, mod in searchResults.items()
                    if any(tag.lower() in mod.get("modTags", []) for tag in filter_tags)
                }

        tags = {
            "clientSide": "Client Side",
            "serverSide": "Server Side",
            "libs": "Libraries",
            "cosmetics": "Cosmetics",
            "fish": "Fish",
            "maps": "Maps",
            "misc": "Misc",
            "mods": "Mods",
            "species": "Species",
            "tools": "Libraries",
        }

        if modTag != "all":
            searchResults = {
                mod_id: mod for mod_id, mod in searchResults.items()
                if tags[modTag].lower() in [tag.lower() for tag in mod.get("modTags", [])]
            }

        completeMods = {}
        for mod_id, mod_data in searchResults.items():
            mod_name = mod_data["modName"].lower()

            if mod_name not in completeMods:
                completeMods[mod_name] = mod_data
            else:
                existing_mod = completeMods[mod_name]
                if mod_data.get("modScore", 0) > existing_mod.get("modScore", 0) or (
                    mod_data.get("modScore", 0) == existing_mod.get("modScore", 0) and
                    mod_data.get("totalDownloads", 0) > existing_mod.get("totalDownloads", 0)):
                    completeMods[mod_name] = mod_data

        return completeMods

    def searchModFolders(self, folderName: str):
        subs = []
        for dirpath, dirnames, _ in os.walk(installationPath + "\\GDWeave\\mods"):
            for dirname in dirnames:
                subs.append(os.path.join(dirpath, dirname))
    
        for folder in subs:
            if os.path.basename(folder) == folderName:
                return folder
    
        threshold = 0.1  # initial threshold
    
        while threshold >= 0.5:
            closestFolder = get_close_matches(folderName, [os.path.basename(folder) for folder in subs], n=1, cutoff=threshold)
            if closestFolder:
                for folder in subs:
                    if os.path.basename(folder) == closestFolder[0]:
                        return folder
            threshold -= 0.01  # lower the threshold gradually if no match is found
    
        return None

    def downloadMod(self, mod: str):
        print(f"Downloading {mod}...")    
        ignoredDependencies = [
            "Pyoid-Hook_Line_and_Sinker",
            "NotNet-GDWeave"
        ]

        modInfo = self.modsList[mod]
            
        print(modInfo)

        modName = modInfo["modName"]
        modAuthor = modInfo["modAuthor"]
        modVersion = modInfo["latestVersion"]
        modDownload = modInfo["latestDownload"]
        modDependencies = modInfo["latestDependencies"]

        if mod not in self.modsBeingDownloaded:
            if self.modsBeingDownloaded.count == 5:
                pymsgbox.alert(
                    title="Mod n' Rod",
                    text=f"The max mods to be downloaded simultaneously (5) has been reached.\nPlease try again later once mods are installed!" + " "*30
                )
                return 

            self.modsBeingDownloaded.append(mod)
            modInfo = self.modsList[mod]

            if modDependencies != []:
                for dependency in modDependencies:
                    dp = dependency.split("-")
                    newDependencyName = f"{dp[0]}-{dp[1]}"
                    reqDependencyVersion = dp[2] #unused for now, but this is the dependency version required by the mod

                    dependencyInfo = self.modsList[newDependencyName]
                    print(f"Checking if Required Dependency is installed...")
                    
                    dependencyName = dependencyInfo["modName"]
                    dependencyAuthor = dependencyInfo["modAuthor"]
                    dependencyVersion = dependencyInfo["latestVersion"]
                    dependencyDownload = dependencyInfo["latestDownload"]
                    dependencyPath = self.searchModFolders(newDependencyName)

                    if newDependencyName not in ignoredDependencies:
                        # handle if dependency is installed or not, and if its on the latest.
                        if dependencyPath:
                            with open(dependencyPath + "\\rnmInfo.json", "r") as f:
                                mnrInfo = load(f)
                            
                            if mnrInfo["version"] != dependencyVersion:
                                download(dependencyDownload, installationPath + "\\GDWeave\\mods", {"name": dependencyName, "author": dependencyAuthor, "version": dependencyVersion})

                        else:
                            download(dependencyDownload, installationPath + "\\GDWeave\\mods", {"name": dependencyName, "author": dependencyAuthor, "version": dependencyVersion})
                            
            # since mod names are completely different we should scan for it and compare
            modPath = self.searchModFolders(modAuthor + "." + modName)

            if modPath:
                try:
                    if modPath != None:
                        with open(modPath + "\\rnmInfo.json", "r") as f:
                            mnrInfo = load(f)

                        if mnrInfo["version"] != modVersion:
                            download(modDownload, installationPath + "\\GDWeave\\mods", {"name": modName, "author": modAuthor, "version": modVersion})
                        else:
                            pymsgbox.alert(
                                title="Mod n' Rod",
                                text=f"{modName} is currently up to date!" + " "*30
                            )

                except FileNotFoundError: # mnrInfo.json missing, skip version check and download mod immediately instead
                    download(modDownload, installationPath + "\\GDWeave\\mods", {"name": modName, "author": modAuthor, "version": modVersion})

            else:
                download(modDownload, installationPath + "\\GDWeave\\mods", {"name": modName, "author": modAuthor, "version": modVersion})

            self.modsBeingDownloaded.remove(mod)
        else:
            pymsgbox.alert(
                title="Mod n' Rod",
                text=f"{modName} is already being downloaded!" + " "*30
            )

    def uninstallMod(self, mod: str, checkExists: bool = False):
        mod = self.searchModFolders(mod)
        
        if checkExists: # check only
            if mod != None:
                return True
            else:
                return False
        else:
            print(f"Uninstalling {mod}...")
            try:
                shutil.rmtree(mod)
            except TypeError: pass
            except PermissionError:
                pymsgbox.alert(
                    title="Mod n' Rod", 
                    text="Permission denied! Please close the game first to uninstall the mod!"
                )

rnm = RodNMod()

if __name__ == "__main__":
    if installationPath == None:
        pymsgbox.alert(
            title="Mod n' Rod",
            text=f"WEBFISHING Installation not found!" + " "*30
        )
    else:     
        try: os.rename(installationPath + "\\GDWeave\\disabled.mods", installationPath + "\\GDWeave\\mods")
        except FileNotFoundError: pass

        with open(resource("./data/config.json")) as file:
            config = load(file)

        window = create_window(
            "Rod n' Mod",
            resource("main.html"),
            width=1080, height=720,
            frameless=True,
            js_api=RodNMod,
        )

        for name in dir(rnm):
            func = getattr(rnm, name)
            if callable(func) and not name.startswith("_"):
                window.expose(func)

        gdweaveLib = rnm.searchModList("GDWeave", "none", "all", False)["gdweave"]
        name, version, downloadUrl = gdweaveLib["modName"], gdweaveLib["latestVersion"], gdweaveLib["latestDownload"]

        if os.path.exists(installationPath + "\\GDWeave") and os.path.isdir(installationPath + "\\GDWeave"):
            print("gdweave installed. check for updates")
            try:
                with open(installationPath + "\\rnmInfo.json") as file:
                    rnmInfo = load(file)

                if rnmInfo["version"] != version:
                    print("GDWeave update available")
                    Thread(target=downloadRaw, args=(downloadUrl, installationPath, {"name": name, "version": version})).start()
                else:
                    print("no GDWeave update available")
            except FileNotFoundError:
                print("rnm gdweave version file info not found")
                Thread(target=downloadRaw, args=(downloadUrl, installationPath, {"name": name, "version": version})).start()

        else:
            print("downloading", downloadUrl)
            Thread(target=downloadRaw, args=(downloadUrl, installationPath, {"name": name, "version": version})).start()

        start(debug=config["debugMode"], icon="/assets/rodnmod.ico")
