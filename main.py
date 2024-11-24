# powered by hopes and dreams

import sys
import string
import logging
from time import sleep
from random import choices
from pyperclip import copy
from json import load, dump
from subprocess import run
from threading import Thread
from datetime import datetime
from rapidfuzz import fuzz, process
from webbrowser import open as openWeb
from shutil import rmtree, copy as copyFile
from re import IGNORECASE, compile as comp
from psutil import process_iter, NoSuchProcess
from os import path, rename, walk, chdir, listdir, makedirs, execv, remove, environ, getcwd

from webview import create_window, start
from webview.errors import JavascriptException

from rodnmod.fishfinder import findWebfishing
from rodnmod.internet import getMods, download

logging.basicConfig(
    level=logging.ERROR,
    filename="rodnmod.log",
    format="%(asctime)s - Application %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


installationPath = findWebfishing()
logging.info(f"Detected Webfishing installation path: {installationPath}")

saveFiles = path.expandvars(r"%AppData%\Godot\app_userdata\webfishing_2_newver")

def exceptHook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = exceptHook

class RodNMod:
    modsList = getMods()
    modsBeingDownloaded = []
    
    def visitSite(self, site: str):
        try: openWeb(site)
        except TypeError: pass

    def launchWebfishing(self, vanilla: bool = False):
        gameExec = path.join(installationPath, 'webfishing.exe')
        tempEnv = environ.copy()
        tempEnv["GDWEAVE_FOLDER_OVERRIDE"] = getcwd() + "\\data\\mods\\GDWeave"
        
        if vanilla:
            run([gameExec, '--gdweave-disable'])
        else:
            run([gameExec], env=tempEnv)

    def copyLogs(self):
        with open("rodnmod.log", 'r') as file:
            content = file.read()
        copy(content)
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
                "savebackups": "save",
                "reelsound": "reel",
                "transition": "transition",
                "filter": "none",
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
    
    def minimizeApplication(self):
        window.minimize()

    def closeApplication(self):
        window.destroy()

    def restartApplication(self):
        if getattr(sys, 'frozen', False):
            execv("./rodnmod.exe", ["./rodnmod.exe"])
        else: # restart in development environment so you can immediately restart the entire code once its updated
            execv(sys.executable, ['python'] + sys.argv)

    # Mods

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

        # this is absolutely not the way you do it strupid idito!!!! check pyoid dms
        # attempt finding mods downloaded from other mod managers.
        # most likely unnamed mod files thats only been installed and extracted
        try: mods = [entry for entry in listdir(installationPath + "\\GDWeave\\mods") if path.isdir(path.join(installationPath + "\\GDWeave\\mods", entry))]
        except FileNotFoundError: mods = [entry for entry in listdir(installationPath + "\\GDWeave\\disabled.mods") if path.isdir(path.join(installationPath + "\\GDWeave\\disabled.mods", entry))]
        
        if self.configure("unprocessedmods") == "findnonrnm" and mods != []:
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
        logging.info(f"Downloading {mod}...")    
        ignoredDependencies = [
            "Pyoid-Hook_Line_and_Sinker",
            "PawsBeGamin-HLSReborn",
            "NotNet-GDWeave"
        ]

        modInfo = self.modsList[mod]
            
        logging.info(modInfo)

        modName = modInfo["modName"]
        modAuthor = modInfo["modAuthor"]
        modVersion = modInfo["latestVersion"]
        modDownload = modInfo["latestDownload"]
        modDependencies = modInfo["latestDependencies"]

        if mod not in self.modsBeingDownloaded:
            if self.modsBeingDownloaded.count == 5:
                window.evaluate_js(f"notify('The limit of 5 mods to be downloaded simultaneously has been reached. Please try again later!', 3000)")
                return 

            self.modsBeingDownloaded.append(mod)
            modInfo = self.modsList[mod]

            if modDependencies != []:
                for dependency in modDependencies:
                    dp = dependency.split("-")
                    newDependencyName = f"{dp[0]}-{dp[1]}"

                    dependencyInfo = self.modsList[newDependencyName]
                    logging.info(f"Checking if Required Dependency is installed...")
                    
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
                                # cant do anything about this, probbably a mod installed via another mod manager like HLS.
                                # maybe once the modding community just comes togehter and make proper and similar
                                # manifest files then i dont have to keep adding more data to mods.
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
        else:
            window.evaluate_js(f"notify('{modName} is already being downloaded!', 3000)")

        return "done"


    def uninstallMod(self, mod: str, checkExists: bool = False):
        modpath = self.searchModFolders(mod)

        if checkExists: # check only
            if modpath != None: return True
            else: return False
        else:
            logging.info(f"Uninstalling {mod}...")
            try:
                rmtree(modpath)
                try: modname = mod.split(".")[1].replace("_", " ")
                except: modname = mod
                window.evaluate_js(f"notify('{modname} has been successfully deleted!', 3000)")
            except PermissionError:
                window.evaluate_js(f"notify('Permission denied! Please close WEBFISHING first to uninstall the mod!', 3000)")
        return "done"
        

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

    # Modpacks
    
    # currently none


    # Save Manager

    def getSavesList(self):
        makedirs("data/savefiles/backups", exist_ok=True)
        folderPath = 'data/savefiles/backups/'

        files = []
        for filename in listdir(folderPath):
            filePath = path.join(folderPath, filename)
            if path.isfile(filePath) and filename.endswith('.sav'):
                creationTime = path.getctime(filePath)
                files.append({
                    'filename': filename,
                    'creationTime': datetime.fromtimestamp(creationTime).strftime('%Y-%m-%d %I:%M:%S %p')
                })

        files.sort(key=lambda x: x['creationTime'], reverse=True)
        return files
    
    def backupSave(self, slot: int = 0):
        makedirs("data/savefiles/backups", exist_ok=True)

        if path.exists(saveFiles):
            try:
                if path.isfile(saveFiles + f"\\webfishing_save_slot_{slot}.sav"):
                    code = ''.join(choices(string.ascii_uppercase, k=5))

                    copyFile(saveFiles + f"\\webfishing_save_slot_{slot}.sav", f"data/savefiles/backups/BACKUP-{code}-SLOT-{slot + 1}.sav")
                    window.evaluate_js(f'generateSaveItems();')
                    window.evaluate_js(f'notify("Backed up Save Slot {slot + 1}!", 3000)')
                else:
                    window.evaluate_js(f'notify("No save found in slot {slot + 1}!")')
            except Exception as e:
                window.evaluate_js(f'notify("Failed to backup. Please check logs!", 3000)')
        
    
    def loadSave(self, saveFile: str):
        if path.exists(saveFiles):
            try:
                if path.isfile(f"data/savefiles/backups/{saveFile}"):
                    slot = int(saveFile.split("-")[3].replace(".sav", "")) - 1
                    copyFile(f"data/savefiles/backups/{saveFile}", saveFiles + f"\\webfishing_save_slot_{slot}.sav")
                    window.evaluate_js(f'notify("Loaded backup for Slot {slot + 1}!", 3000)')
                else:
                    window.evaluate_js(f'notify("Local Save File does not exist.")')
            except Exception as e:
                window.evaluate_js(f'notify("Failed to load Save File. Please check logs!", 3000)')

    def deleteSave(self, saveFile: str):
        if path.exists(saveFiles):
            try:
                if path.isfile(f"data/savefiles/backups/{saveFile}"):
                    remove(f"data/savefiles/backups/{saveFile}")
                    window.evaluate_js(f'generateSaveItems();')
                    slot = saveFile.split("-")[3].replace(".sav", "")
                    window.evaluate_js(f'notify("Deleted backup for Slot {slot}.")')
                else:
                    window.evaluate_js(f'notify("Local Save File does not exist.")')
            except Exception as e:
                window.evaluate_js(f'notify("Failed to delete Save File. Please check logs!", 3000)')

class WindowFunctions:
    sceneChanging = False
    settingsDisplayed = False
    state = ""
    
    def checkRunning():
        launchButtons = window.dom.get_element(".run")
        while True:
            try:
                WindowFunctions.state = any(proc.name() == "webfishing.exe" for proc in process_iter())
            except NoSuchProcess:
                WindowFunctions.state = False
            
            try:
                if WindowFunctions.state:
                    launchButtons.style["opacity"] = 0
                    launchButtons.style["pointerEvents"] = "none"
                else:
                    launchButtons.style["opacity"] = 1
                    launchButtons.style["pointerEvents"] = "all"
                sleep(0.05)
            except JavascriptException:
                pass
    
    # reloading the page wouldn't trigger this at all, so your best bet is to
    # just restart the application by pressing escape 3 times
    def onLoad():
        splashText = window.dom.get_element("#splashText")
        
        # Window Buttons
        splashText.text = "Setting Button Events"
        window.dom.get_element(".minimizeButton").events.click += lambda e: window.minimize()
        window.dom.get_element(".closeButton").events.click += lambda e: (
            WindowFunctions.content(".content"),
            sleep(3),
            window.destroy()
        )

        splashText.text = "Starting Background Processes"
        # Background Processes n stuff
        Thread(target=WindowFunctions.checkRunning, daemon=True).start()
        
        splashText.text = "Setting Configs"
        # Configurations
        configs = [
            "debugging",
            "savebackups",
            "reelsound",
            "transition",
            "filter",
            "category",
            "nsfw"
        ]

        for config in configs:
            value = rnm.configure(config)
            splashText.text = f"set config: {config} -> {value}"
            window.evaluate_js(f'setDropdownValue("{config}", "{value}")')

        if installationPath != None: 
            splashText.text = "Starting Rod n\\' Mod..."
            window.evaluate_js(f"handleChange();")
            window.evaluate_js(f"generateSaveItems();")
            sleep(1)
            window.evaluate_js(f"openWindow();") 
        else:
            splashText.text = "ERROR: Webfishing Installation not Found. USE MANUAL PATH OVERRIDE CONFIG!!"

    def content(element: str = None, visibility: str = "hide"):
        if visibility == "hide":
            window.dom.get_element(element).style["clipPath"] = r"circle(0% at 50% 50%)"
            window.evaluate_js("playAudio('/assets/web/fishing/sounds/guitar_in.ogg');")
        else:
            window.dom.get_element(element).style["clipPath"] = r"circle(75% at 50% 50%)"
            window.evaluate_js("playAudio('/assets/web/fishing/sounds/guitar_out.ogg');")

rnm = RodNMod()

if __name__ == "__main__":
    window = create_window(
        "Rod n' Mod",
        "main.html",
        width=1200, height=800,
        frameless=True,
        easy_drag=True,
        js_api=RodNMod,
    )

    for name in dir(rnm):
        func = getattr(rnm, name)
        if callable(func) and not name.startswith("_"):
            window.expose(func)

    debugOption = True if rnm.configure("debugging") == "debena" else False
    window.events.loaded += lambda: window.evaluate_js(f"scriptsReady();")
    start(WindowFunctions.onLoad, debug=debugOption)

    