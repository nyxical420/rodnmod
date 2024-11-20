import sys
import semver
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
    filename="rodnmod.log",
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
    def doUpdates():
        status = window.dom.get_element("#status")
        status.text = "Checking for Updates..."
        rnm = get("https://api.github.com/repos/nyxical420/rodnmod/releases?per_page=1").json()[0]
        
        with open("version.json") as ver:
            version = load(ver)

        for x in rnm["assets"]:
            if str(x["name"]).__contains__("rodnmod-standalone"):
                asset = x
        
        if semver.compare(version["version"], rnm["tag_name"]) < 0:
            newver = rnm["tag_name"]
            curver = version["version"]
            status.text = f"Downloading Update...\n{curver} -> {newver}"

            response = get(asset["browser_download_url"], follow_redirects=True)

            if response.status_code == 200:
                with open("update.zip", 'wb') as f:
                    f.write(response.content)
                status.text = "Unpacking Update...\nPlease wait for the updater to re-run!"

                execv("./rnmunpacker.exe", ["./rnmunpacker.exe"])
            else:
                status.text = f"Failed to download update.\nHTTP Status Code: {response.status_code}"
            
        elif semver.compare(version["version"], rnm["tag_name"]) > 0:
            print("Version is greater than remote version. This is a Development Build.")

        if installationPath != None:
            gdweaveLib = getMods()["NotNet-GDWeave"]
            name, version, downloadUrl = gdweaveLib["modName"], gdweaveLib["latestVersion"], gdweaveLib["latestDownload"]

            if path.exists(installationPath + "\\GDWeave") and path.isdir(installationPath + "\\GDWeave"):
                status.text = "Checking for GDWeave Update..."
                try:
                    with open(installationPath + "\\rnmInfo.json") as file:
                        rnmInfo = load(file)

                    if rnmInfo["version"] != version:
                        rnmv = rnmInfo["version"]
                        status.text = "Updating GDWeave..."
                        window.evaluate_js(f"{status}.innerHTML = \"Updating GDWeave<br>{rnmv} -> {version}\"")
                        downloadRaw(downloadUrl, installationPath, {"name": name, "version": version})
                    else:
                        status.text = "No GDWeave Updates Available..."
                except FileNotFoundError:
                    status.text = "Reinstalling GDWeave...\n(Rod n\\' Mod versioning compatibility)"
                    downloadRaw(downloadUrl, installationPath, {"name": name, "version": version})
            else:
                status.text = "Downloading GDWeave..."
                downloadRaw(downloadUrl, installationPath, {"name": name, "version": version})
        
        status.text = "Launching Rod n\\' Mod"
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

    window.events.loaded += RodNModUpdater.doUpdates
    start()