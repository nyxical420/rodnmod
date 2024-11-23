<p align="center">
    <img src="https://github.com/nyxical420/rodnmod/blob/main/assets/repository/banner.png?raw=true" width="800"/><br>
    A webfishing-themed AND tailored mod manager!
</p>

<p align="center">
    <img src="https://github.com/nyxical420/rodnmod/blob/main/assets/repository/divisor.png?raw=true" width="800"/><br>
</p>

> [!NOTE]
> Assets located in `assets/web/fishing` are WEBFISHING game assets and is excepted from the project's license.

> [!WARNING]  
> Rod n' Mod is still on it's alpha stage, so there may be bugs and issues. If you encounter any, please report them to me in the [issues page](https://github.com/nyxical420/rodnmod/issues) or at my discord! (@nyxical ID:583200866631155714)

> [!NOTE]
> Rod n' Mod is incompatible to [Hook, Line, & Sinker](https://hooklinesinker.lol). (uncertain: r2mm, GMM) due to how HLS and Rod n' Mod handles installed mods.

# Download
You can download Rod n' Mod here!<br>
### [Download Rod n' Mod](https://github.com/nyxical420/rodnmod/releases/latest)

# Features
- **Launch Vanilla/Modded**: Launch WEBFISHING with or without mods!
- **Mod Manager**: Install, update, and uninstall mods easily!
- **Modpacks**: Easily create and share modpacks to others!
- **Save Manager**: Easily backup and restore your WEBFISHING saves!
- **Installation Detection**: Automatically finds your WEBFISHING installation! no need to configure the installation path!

# Requirements
- A webview runtime. I recommend having [Microsoft Edge WebView2 Runtime](https://developer.microsoft.com/en-gb/microsoft-edge/webview2#download) for Windows (OPTIONAL, ALTHOUGH RECOMMENDED STILL), and `libwebkit2gtk-4.1-dev` for Linux. (no official Linux support yet) (SOON!!!)

# Building Rod n' Mod
> [!IMPORTANT]
> Building Rod n' Mod requires Python 3.11.0.

> [!IMPORTANT]
> Make sure you build Rod n' Mod in a virtual environment!

To build Rod n' Mod, you will need to initialize a Virtual Environment and installed the required libraries with:
(Powershell)
```PS
python -m venv .venv; .\.venv\Scripts\Activate; pip install -r requirements.txt
```

Once the command is done, you should see a (.venv) in your terminal. This means that the virtual environment is activated. and you can proceed to run the build script:
```PS
python setup.py build
```

This should automatically build Rod n' Mod for you and put the final build at the root folder.


# Troubleshooting / Known Bugs & Stuff
- There are currently no known existing bugs.

# Credits
- @zoiudolo for Rod n' Mod Logo, Banner, and Images/Icons
- west for Game Sounds and Cursor used in Rod n' Mod

<p align="center">
    <img src="https://github.com/nyxical420/rodnmod/blob/main/assets/repository/enddivisor.png?raw=true" width="800"/><br>
</p>