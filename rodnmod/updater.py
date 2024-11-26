import sys
import semver
import logging
from httpx import get
from json import load
from platform import system
from os import path, chdir, execv,getcwd
from webview import create_window, start

from rodnmod.fishfinder import findWebfishing
from rodnmod.internet import downloadRaw, getMods

installationPath = findWebfishing()

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

def sanitizeVer(version):
    return version.lstrip('v')
class RodNModUpdater:
    def doUpdates():
        status = "document.getElementById('status')"
        window.evaluate_js(f'{status}.innerHTML = "Checking for Updates..."')
        rnm = get("https://api.github.com/repos/nyxical420/rodnmod/releases?per_page=1").json()[0]
        
        with open("version.json") as ver:
            version = load(ver)

        systems = {
            "Windows": "win",
            "Linux": "linux"
        }
        
        userOS = systems[system()]

        asset = None
        for x in rnm["assets"]:
            if str(x["name"]).__contains__(f"rodnmod-standalone-{userOS}.7z"):
                asset = x
        
        remoteVersion = sanitizeVer(rnm["tag_name"])
        localVersion = sanitizeVer(version["version"])

        if asset == None:
            window.evaluate_js(f'{status}.innerHTML = "No update found for your system."')
        else:
            if semver.compare(localVersion, remoteVersion) < 0:
                window.evaluate_js(f'{status}.innerHTML = "Downloading Update...<br>{localVersion} -> {remoteVersion}"')
                response = get(asset["browser_download_url"], follow_redirects=True)

                if response.status_code == 200:
                    with open("update.7z", 'wb') as f:
                        f.write(response.content)

                    window.evaluate_js(f'{status}.innerHTML = "Upacking Update...<br>Please wait for the updater to re-run!"')


                    if system() == 'Windows':
                        execv(r'.\winupdate.bat', ['winupdate.bat'])
                    else:
                        execv(r'.\linuxupdate.sh', ['linuxupdate.sh'])
                else:
                    window.evaluate_js(f'{status}.innerHTML = "Failed to download update.<br>HTTP Status Code: {response.status_code}"')

            elif semver.compare(version["version"], rnm["tag_name"]) > 0:
                print("Version is greater than remote version. This is a Development Build.")

        if installationPath != None:
            gdweaveLib = getMods()["NotNet-GDWeave"]
            name, version, downloadUrl = gdweaveLib["modName"], gdweaveLib["latestVersion"], gdweaveLib["latestDownload"]

            if path.exists("data\modenv\GDWeave") and path.isdir("data\modenv\GDWeave"):
                window.evaluate_js(f'{status}.innerHTML = "Checking for GDWeave Update"')
                try:
                    with open("data\modenv\\rnmInfo.json") as file:
                        rnmInfo = load(file)

                    if rnmInfo["version"] != version:
                        rnmv = rnmInfo["version"]
                        window.evaluate_js(f'{status}.innerHTML = "Updating GDWeave...<br>{rnmv} -> {version}"')
                        downloadRaw(downloadUrl, "data\modenv\\", {"name": name, "version": version})
                    else:
                        window.evaluate_js(f'{status}.innerHTML = "No GDWeave Updates Available..."')
                except FileNotFoundError:
                    window.evaluate_js(f'{status}.innerHTML = "Reinstalling GDWeave...<br>(Rod n\' Mod versioning compatibility)"')
                    downloadRaw(downloadUrl, "data\modenv\\", {"name": name, "version": version})
            else:
                window.evaluate_js(f'{status}.innerHTML = "Downloading GDWeave..."')
                downloadRaw(downloadUrl, "data\modenv\\", {"name": name, "version": version})
        
        window.evaluate_js(f'{status}.innerHTML = "Launching Rod n\' Mod"')
        #if getattr(sys, 'frozen', False):
        #    execv("./rodnmod.exe", ["./rodnmod.exe"])
        #else:
        #    execv(sys.executable, ['python', 'main.py'])
        window.destroy()

rnmu = RodNModUpdater()

def initiate():
    chdir(path.dirname(path.abspath(__name__)))

    global window
    window = create_window(
        "Rod n' Mod Updater",
        path.abspath(path.join(getcwd(), "updater.html")),
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