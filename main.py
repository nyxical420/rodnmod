# powered by hopes and dreams

import sys
import shutil
import pymsgbox
from time import time
from json import load
from functools import wraps
from threading import Thread
from os import path, rename, walk
from rapidfuzz import fuzz, process
from webbrowser import open as openWeb
from re import IGNORECASE, compile as comp
from psutil import process_iter, NoSuchProcess
from webview import create_window, start, windows as webWindows

from rodnmod.fishfinder import findWebfishing
from rodnmod.thunderstore import getMods, download, downloadRaw

webfishingInstalled = False
installationPath = findWebfishing()

if installationPath:
    print(f"Installation Path: {installationPath}")
    webfishingInstalled = True
else:
    print("WEBFISHING Installation Path Not Found")


def resource(rpath):
    if hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS, rpath)
    else:
        return path.join(path.dirname(__file__), rpath)

class RodNMod:
    modsList = getMods()
    modsBeingDownloaded = []

    def isInstalled(self):
        return {"installationStatus": webfishingInstalled}
    
    def dragWindow(self, dx, dy):
        if webWindows:
            window = webWindows[0]
            window.move(window.x + dx, window.y + dy)
    
    def visitSite(self, site: str):
        openWeb(site)

    def launchWebfishing(self, vanilla: bool = False):
        mods_folder = installationPath + "\\GDWeave\\mods"
        disabled_folder = installationPath + "\\GDWeave\\disabled.mods"
        try:
            if vanilla:
                rename(mods_folder, disabled_folder)
            else:
                rename(disabled_folder, mods_folder)
        except FileNotFoundError:
            pass
        self.visitSite("steam://rungameid/3146520")

    def webfishingInstallation(self):
        return installationPath
    
    def minimizeApplication(self):
        window.minimize()

    def closeApplication(self):
        window.destroy()

    def webfishingRunning(self):
        try:
            running = any(proc.name() == "webfishing.exe" for proc in process_iter())
        except NoSuchProcess:
            running = False
        return {"running": running}
    
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
        if not match:
            return 0
        value = int(match.group(1))
        unit_multipliers = {"minute": 1, "hour": 60, "day": 1440}
        return value * unit_multipliers.get(match.group(2).lower().split()[0], 1)
        
    def searchModList(self, searchQuery: str, filter: str, modTag: str, nsfw: bool):
        searchQuery = searchQuery.strip().lower()

        filtered_mods = {
            mod_id: mod for mod_id, mod in self.modsList.items()
            if nsfw or not mod.get("isNSFW", False)
        }

        if not searchQuery:
            searchResults = filtered_mods
        else:
            searchResults = {
                mod_id: mod_data for mod_id, mod_data in filtered_mods.items()
                if (score := fuzz.WRatio(searchQuery, mod_data["modName"].lower())) >= 75
            }

            for mod in searchResults.values():
                mod["fuzz_score"] = fuzz.WRatio(searchQuery, mod["modName"].lower())

            searchResults = dict(sorted(searchResults.items(), key=lambda x: x[1]["fuzz_score"], reverse=True))

        if filter != "none":
            filters = { 
                "installed": lambda x: self.searchModFolders(f"{x[1].get('modAuthor')}.{x[1].get('modName')}") is not None,
                "likesCount": lambda x: x[1].get("modScore", 0),
                "downloadCount": lambda x: x[1].get("totalDownloads", 0),
                "nameA-Z": lambda x: x[1]["modName"].lower(),
                "nameZ-A": lambda x: x[1]["modName"].lower(),
                "mostDownloaded": lambda x: x[1].get("totalDownloads", 0),
                "leastDownloaded": lambda x: x[1].get("totalDownloads", 0),
                "mostLiked": lambda x: x[1].get("modScore", 0),
                "leastLiked": lambda x: x[1].get("modScore", 0),
                "newlyUpdated": lambda x: self.updatedAgo(x[1].get("updatedAgo", "")),
                "leastUpdated": lambda x: self.updatedAgo(x[1].get("updatedAgo", "")),
            }

            if filter in filters:
                reverse = filter in ["installed", "likesCount", "downloadCount", "mostDownloaded", "mostLiked", "newlyUpdated"]
                searchResults = dict(sorted(searchResults.items(), key=filters[filter], reverse=reverse))
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
        for dirpath, dirnames, _ in walk(installationPath + "\\GDWeave\\mods"):
            for dirname in dirnames:
                subs.append(path.join(dirpath, dirname))
        
        for folder in subs:
            if path.basename(folder) == folderName:
                #print(f"found {folderName} as {folder} with exact match")
                return folder

            try: splitted = folderName.split(".")[1]
            except: splitted = folderName.split("-")[1]
            if path.basename(folder) == splitted:
                #print(f"found {folderName} as {folder} with name match")
                return folder
        
        # NOTE: make this a setting to either be turned on/off to reduce processing power
        # attempt finding mods downloaded from HLS.
        transformations = [
            (lambda name: name.split(".")[1] if "." in name else name, 90),  # Use split name
            (lambda name: name.replace("-", "."), 85),                       # Replace '-' with '.'
            (lambda name: name.replace("_", "."), 86)                        # Replace '_' with '.'
        ]
        
        folder_base_names = [path.basename(folder) for folder in subs]
        
        for transform, threshold in transformations:
            transformed_name = transform(folderName)
            closest_folder = process.extractOne(transformed_name, folder_base_names)

            if closest_folder and closest_folder[1] >= threshold:
                matchingFolder = subs[folder_base_names.index(closest_folder[0])]
                #print(f"Found {folderName} as {matchingFolder} with close match of {closest_folder[1]}%")
                return matchingFolder

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
            if self.modsBeingDownloaded.count == 7:
                pymsgbox.alert(
                    title="Rod n' Mod",
                    text=f"The max mods to be downloaded simultaneously (7) has been reached.\nPlease try again later once mods are installed!" + " "*30
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
                            try:
                                with open(dependencyPath + "\\rnmInfo.json", "r") as f:
                                    mnrInfo = load(f)
                            except:
                                # cant do anything about this, probbably a mod installed via HLS.
                                mnrInfo = {"version": "1.0.0"}

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
                                title="Rod n' Mod",
                                text=f"{modName} is currently up to date!" + " "*30
                            )

                except FileNotFoundError: # mnrInfo.json missing, skip version check and download mod immediately instead
                    download(modDownload, installationPath + "\\GDWeave\\mods", {"name": modName, "author": modAuthor, "version": modVersion})

            else:
                download(modDownload, installationPath + "\\GDWeave\\mods", {"name": modName, "author": modAuthor, "version": modVersion})

            self.modsBeingDownloaded.remove(mod)
        else:
            pymsgbox.alert(
                title="Rod n' Mod",
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
                    title="Rod n' Mod", 
                    text="Permission denied! Please close the game first to uninstall the mod!"
                )

rnm = RodNMod()

if __name__ == "__main__":
    if installationPath == None:
        pymsgbox.alert(
            title="Rod n' Mod",
            text=f"WEBFISHING Installation not found!" + " "*30
        )
    else:     
        try: rename(installationPath + "\\GDWeave\\disabled.mods", installationPath + "\\GDWeave\\mods")
        except FileNotFoundError: pass

        with open("./data/config.json") as file:
            config = load(file)

        window = create_window(
            "Rod n' Mod",
            resource("./main.html"),
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

        if path.exists(installationPath + "\\GDWeave") and path.isdir(installationPath + "\\GDWeave"):
            print("gdweave installed. check for updates")
            try:
                with open(installationPath + "\\rnmInfo.json") as file:
                    rnmInfo = load(file)

                if rnmInfo["version"] != version:
                    print("GDWeave update available")
                    Thread(target=pymsgbox.alert, args=("GDWeave is updating in the background. Please wait for Rod n' Mod to finish the update.")).start()
                    downloadRaw(downloadUrl, installationPath, {"name": name, "version": version})
                else:
                    print("no GDWeave update available")
            except FileNotFoundError:
                print("rnm gdweave version file info not found")
                Thread(target=pymsgbox.alert, args=("GDWeave is installing in the background. Please wait for Rod n' Mod to finish the installation.", "Rod n' Mod")).start()
                downloadRaw(downloadUrl, installationPath, {"name": name, "version": version})
        else:
            print("downloading", downloadUrl)
            Thread(target=pymsgbox.alert, args=("GDWeave is installing in the background. Please wait for Rod n' Mod to finish the installation.", "Rod n' Mod")).start()
            downloadRaw(downloadUrl, installationPath, {"name": name, "version": version})

        start(debug=config["debugMode"])