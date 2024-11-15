# powered by hopes and dreams

import sys
import logging
import pyperclip
import subprocess
from shutil import rmtree
from json import load, dump
from rapidfuzz import fuzz, process
from webbrowser import open as openWeb
from re import IGNORECASE, compile as comp
from psutil import process_iter, NoSuchProcess
from webview import create_window, start, windows as webWindows
from os import path, rename, walk, chdir, listdir, makedirs, execv

from rodnmod.fishfinder import findWebfishing
from rodnmod.internet import getMods, download

latestVersion = None
webfishingInstalled = False
installationPath = findWebfishing()

if installationPath:
    print(f"Installation Path: {installationPath}")
    webfishingInstalled = True
else:
    print("WEBFISHING Installation Path Not Found")

chdir(path.dirname(path.abspath(__name__)))

logging.basicConfig(
    level=logging.ERROR,
    filename="rodnmod.log",
    format="%(asctime)s - Application %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def exceptHook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = exceptHook

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

    def copyLogs(self):
        with open("rodnmod.log", 'r') as file:
            content = file.read()
        pyperclip.copy(content)
        window.evaluate_js(f"notify('Logs has been copied!', 3000)")

    def clearLogs(self):
        with open("rodnmod.log", 'w') as file:
            file.write("")
        window.evaluate_js(f"notify('Log File has been cleared!', 3000)")
        
    
    def configure(self, configItem: str, configValue=None):
        makedirs("data", exist_ok=True)

        if not path.exists("data/config.json"):
            with open("data/config.json", "w") as file:
                default_config = {
                "debugging": "debdis",
                "hlsmods": "findhls",
                "reelsound": "reel",
                "transition": "transition",
                "filter": "installed",
                "category": "all",
                "nsfw": "hidensfw"
            }
            with open("data/config.json", 'w') as file:
                dump(default_config, file, indent=4)

        with open("data/config.json", "r") as file:
            config = load(file)

        if configValue is None:
            return config.get(configItem, "Not a configuration item")
        else:
            config[configItem] = configValue
            with open("data/config.json", 'w') as file:
                dump(config, file, indent=4)
            return "Configured!"

    def webfishingInstallation(self):
        return installationPath
    
    def minimizeApplication(self):
        window.minimize()

    def closeApplication(self):
        window.destroy()

    def restartApplication(self):
        execv("./rodnmod.exe", ["./rodnmod.exe"])


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
        
    def searchModList(self, searchQuery: str, filter: str, modTag: str, nsfw):
        searchQuery = searchQuery.strip().lower()
        nsfw = False if nsfw == "hidensfw" else True

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
                return folder

            try: splitted = folderName.split(".")[1]
            except: splitted = folderName.split("-")[1]
            if path.basename(folder) == splitted:
                return folder
        
        # attempt finding mods downloaded from HLS.
        mods = [entry for entry in listdir(installationPath + "\\GDWeave\\mods") if path.isdir(path.join(installationPath + "\\GDWeave\\mods", entry))]
        if self.configure("hlsmods") == "findhls" and mods != []:
            transformations = [
                (lambda name: name.split(".")[1] if "." in name else name, 90),
                (lambda name: name.replace("-", "."), 85),
                (lambda name: name.replace("_", "."), 86)
            ]

            folder_base_names = [path.basename(folder) for folder in subs]

            for transform, threshold in transformations:
                transformed_name = transform(folderName)
                closest_folder = process.extractOne(transformed_name, folder_base_names)

                if closest_folder and closest_folder[1] >= threshold:
                    matchingFolder = subs[folder_base_names.index(closest_folder[0])]
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
                window.evaluate_js(f"notify('The limit of 7 mods to be downloaded simultaneously has been reached. Please try again later!', 3000)")
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
                                    rnmInfo = load(f)
                            except:
                                # cant do anything about this, probbably a mod installed via HLS.
                                rnmInfo = {"version": "1.0.0"}

                            if rnmInfo["version"] != dependencyVersion:
                                download(dependencyDownload, installationPath + "\\GDWeave\\mods", {"name": dependencyName, "author": dependencyAuthor, "version": dependencyVersion})

                        else:
                            download(dependencyDownload, installationPath + "\\GDWeave\\mods", {"name": dependencyName, "author": dependencyAuthor, "version": dependencyVersion})
                            
            # since mod names are completely different we should scan for it and compare
            modPath = self.searchModFolders(modAuthor + "." + modName)

            if modPath:
                try:
                    if modPath != None:
                        with open(modPath + "\\rnmInfo.json", "r") as f:
                            rnmInfo = load(f)

                        if rnmInfo["version"] != modVersion:
                            download(modDownload, installationPath + "\\GDWeave\\mods", {"name": modName, "author": modAuthor, "version": modVersion})
                            window.evaluate_js(f"notify('{modName} has been updated successfully!', 3000)")
                        else:
                            window.evaluate_js(f"notify('{modName} is currently up to date!', 3000)")

                except FileNotFoundError: # rnmInfo.json missing, skip version check and download mod immediately instead
                    window.evaluate_js(f"notify('rnmInfo.json for {modName} missing. Forcing download...', 3000)")
                    download(modDownload, installationPath + "\\GDWeave\\mods", {"name": modName, "author": modAuthor, "version": modVersion})

            else:
                download(modDownload, installationPath + "\\GDWeave\\mods", {"name": modName, "author": modAuthor, "version": modVersion})
                window.evaluate_js(f"notify('{modName} has been downloaded successfully!', 3000)")

            self.modsBeingDownloaded.remove(mod)
            return "done"
        else:
            window.evaluate_js(f"notify('{modName} is already being downloaded!', 3000)")


    def uninstallMod(self, mod: str, checkExists: bool = False):
        modpath = self.searchModFolders(mod)

        if checkExists: # check only
            if modpath != None:
                return True
            else:
                return False
        else:
            print(f"Uninstalling {mod}...")
            try:
                rmtree(modpath)
                try: modname = mod.split(".")[1].replace("_", " ")
                except: modname = mod
                window.evaluate_js(f"notify('{modname} has been successfully deleted!', 3000)")

            except TypeError: pass
            except PermissionError:
                window.evaluate_js(f"notify('Permission denied! Please close WEBFISHING first to uninstall the mod!', 3000)")

    def updateAllMods(self):
        window.evaluate_js(f"notify('Updating Mods...', 3000)")
        fpath = installationPath + "\\GDWeave\\mods"

        try: folders = [entry for entry in listdir(fpath) if path.isdir(path.join(fpath, entry))]
        except:
            window.evaluate_js(f"notify('Could not update mods. (Mods folder missing in GDWeave directory)', 3000)")
            return

        for mod in folders:
            try: mod = mod.split(".")[1]
            except IndexError: pass
            _, value = next(iter(self.searchModList(mod, "none", "all", "shownsfw").items()))

            try:
                with open(f"{fpath}\\" + value.get("modAuthor") + "." + value.get("modName") + "\\rnmInfo.json", "r") as f:
                    modInfo = load(f)
            except FileNotFoundError:
                modInfo = {"version": "null"}

            if value.get("latestVersion") != modInfo["version"]:
                self.downloadMod(value.get("modAuthor") + "-" + value.get("modName"))

        window.evaluate_js(f"notify('Updated all mods!', 3000)")


rnm = RodNMod()

if __name__ == "__main__":
    makedirs(installationPath + "\\GDWeave\\mods", exist_ok=True)

    window = create_window(
        "Rod n' Mod",
        "main.html",
        width=1200, height=800,
        frameless=True,
        js_api=RodNMod,
    )

    for name in dir(rnm):
        func = getattr(rnm, name)
        if callable(func) and not name.startswith("_"):
            window.expose(func)

    debugOption = True if rnm.configure("debugging") == "debena" else False
    start(debug=debugOption)