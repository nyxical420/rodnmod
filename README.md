<p align="center">
    <img src="https://github.com/nyxical420/rodnmod/blob/main/assets/web/banner.png?raw=true" width="800"/><br>
    A webfishing-themed mod manager!
</p>

> [!WARNING]  
> Rod n' Mod is still on it's alpha stage, so there may be bugs and issues. If you encounter any, please report them to me in the [issues page](https://github.com/nyxical420/rodnmod/issues) or at my discord! (@nyxical ID:583200866631155714)

> [!NOTE]
> Rod n' Mod handles mods differently than [Hook Line and Sinker](https://hooklinesinker.lol)! so mods installed through HLS may not be detected from Rod n' Mod.
> It still attempts to find mods installed through HLS, but the detection accuracy is not guaranteed to be 100%. This also means it also uses **LOTS** of CPU resources to find them apparently... (jank code 🔥)

## why?
i was bored... and it looks cool tbh

# Download
You can download Rod n' Mod here!<br>
https://github.com/nyxical420/rodnmod/releases

# Features
- **Launch Options**: Launch WEBFISHING with or without mods!
- **Mod Manager**: Install, update, and uninstall mods easily!
- **Installation Detection**: Automatically finds your WEBFISHING installation! no need to configure anything!

# Requirements
- A webview runtime. I recommend having [Microsoft Edge WebView2 Runtime](https://developer.microsoft.com/en-gb/microsoft-edge/webview2#download) for Windows, and `libwebkit2gtk-4.1-dev` for Linux.

# Building Rod n' Mod
> [!IMPORTANT]
> Building Rod n' Mod requires Python 3.11.0.

To build Rod n' Mod, you will need to initialize a Virtual Environment and installed the required libraries with:
(Powershell)
```PS
python -m venv .venv; .\.venv\Scripts\Activate; pip install -r requirements.txt
```

Once the command is done, you should see a (.venv) in your terminal. This means that the virtual environment is activated. and you can proceed to run the build script:
```PS
python build.py
```

This should automatically build Rod n' Mod for you and put the final build at the root folder.


# Troubleshooting / Known Stuff
- If Rod n' Mod doesn't close the splash screen, try exiting with ALT + F4 and relaunch Rod n' Mod.
    - This is a rare-ish occurence where pywebview api just can't be accessed on launch. It still tries to save you by refreshing the page though, although not a guarantee.
    - If you happen to have debugging enabled, please send me the webview error log!
- If it takes a while for you to install mods, try relaunching Rod n' Mod.
- Mods may not be detected by Rod n' Mod if installed from [HLS](https://hooklinesinker.lol/) because of how different Rod n' Mod handles installing/detecting mods.

# Credits
- @zoiudolo for Rod n' Mod Logo, Banner, and Images/Icons
- west for Game Sounds and Cursor used in Rod n' Mod