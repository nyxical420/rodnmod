import sys
import logging
from httpx import get
from json import load
from os import path, chdir, execv
from webview import create_window, start

from rodnmod.fishfinder import findWebfishing
from rodnmod.internet import downloadRaw, getMods

installationPath = findWebfishing()

chdir(path.dirname(path.abspath(__name__)))

logging.basicConfig(
    level=logging.ERROR,
    filename="error.log",
    format="%(asctime)s - Updater %(levelname)s " + "-"*15,
    datefmt="%Y-%m-%d %H:%M:%S"
)

def exceptHook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = exceptHook
class RodNModUpdater:
    def doUpdates(self):
        status = "document.getElementById('status')"
        window.evaluate_js(f"{status}.innerHTML = 'Checking for Updates...'")
        rnm = get("https://api.github.com/repos/nyxical420/rodnmod/releases?per_page=1").json()[0]
        
        with open("version.json") as ver:
            version = load(ver)

        for x in rnm["assets"]:
            if str(x["name"]).__contains__("rodnmod-standalone"):
                asset = x
        
        if version["version"] != rnm["tag_name"]:
            newver = asset["tag_name"]
            curver = rnm["version"]
            window.evaluate_js(f"{status}.innerHTML = \"Downloading Update...<br>{curver} -> {newver}\"")
            #downloadRaw(asset["browser_download_url"], "./")
            window.evaluate_js(f"{status}.innerHTML = 'Update Downloaded!'")
        
        if installationPath != None:
            gdweaveLib = getMods()["NotNet-GDWeave"]
            name, version, downloadUrl = gdweaveLib["modName"], gdweaveLib["latestVersion"], gdweaveLib["latestDownload"]

            if path.exists(installationPath + "\\GDWeave") and path.isdir(installationPath + "\\GDWeave"):
                window.evaluate_js(f"{status}.innerHTML = 'Checking for GDWeave Update...'")
                try:
                    with open(installationPath + "\\rnmInfo.json") as file:
                        rnmInfo = load(file)

                    if rnmInfo["version"] != version:
                        rnmv = rnmInfo["version"]
                        window.evaluate_js(f"{status}.innerHTML = \"Updating GDWeave<br>{rnmv} -> {version}\"")
                        downloadRaw(downloadUrl, installationPath, {"name": name, "version": version})
                    else:
                        window.evaluate_js(f"{status}.innerHTML = 'No GDWeave Updates Available...'")
                except FileNotFoundError:
                    window.evaluate_js(f"{status}.innerHTML = \"Reinstalling GDWeave...<br>(For Rod n' Mod versioning compatibility)\"")
                    downloadRaw(downloadUrl, installationPath, {"name": name, "version": version})
            else:
                window.evaluate_js(f"{status}.innerHTML = 'Downloading GDWeave...'")
                downloadRaw(downloadUrl, installationPath, {"name": name, "version": version})
            
        window.evaluate_js(f"{status}.innerHTML = \"Launchiung Rod n' Mod...\"")
        execv("./rodnmod.exe", ["./rodnmod.exe"])

rnmu = RodNModUpdater()

if __name__ == "__main__":
    window = create_window(
        "Rod n' Mod Updater",
        "updater.html",
        width=380, height=450,
        frameless=True,
        js_api=RodNModUpdater,
    )

    for name in dir(rnmu):
        func = getattr(rnmu, name)
        if callable(func) and not name.startswith("_"):
            window.expose(func)

    start()