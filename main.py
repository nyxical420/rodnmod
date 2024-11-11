# powered by hopes and dreams

import sys
from os import path
from pymsgbox import alert
from webview import create_window, start

from rodnmod.fishfinder import findWebfishing

webfishingInstalled = False
installationPath = findWebfishing()

def resource(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return path.join(sys._MEIPASS, relative_path)
    else:
        return path.join(path.dirname(__file__), relative_path)

class RodNMod:
    def webfishingInstallation(self):
        return installationPath
    
    def minimizeApplication(self):
        window.minimize()

    def closeApplication(self):
        window.destroy()
        

rnm = RodNMod()

if __name__ == "__main__":
    if installationPath == None:
        alert(
            title="Rod n' Mod",
            text=f"WEBFISHING Installation not found!" + " "*30
        )
    else:
        window = create_window(
            "Rod n' Mod Updater",
            resource("updater.html"),
            width=350, height=400,
            frameless=True,
            js_api=RodNMod,
        )

        for name in dir(rnm):
            func = getattr(rnm, name)
            if callable(func) and not name.startswith("_"):
                window.expose(func)

        start(debug=False)
        
        with open(resource("./rodnmod/app.py")) as script:
            script = script.read()
            exec(script)