document.body.style.zoom = '0.85';

let sceneChanging = false;
let previousIsRunning = null;
const preloadedAudio = {};  // Store preloaded audio objects

function showResponse(response) {
    var container = document.getElementById('res');
    container.textContent = response;
    container.style.display = 'block';
}

function updateModsCount() {
    const elements = document.querySelectorAll(".item");
    const topCountView = document.getElementById("mct");
    const bottomCountView = document.getElementById("mcb");

    let topCount = 0;
    let bottomCount = 0;

    elements.forEach(element => {
        const rect = element.getBoundingClientRect();

        if (rect.bottom < 34) {
            topCount++;
        }

        if (rect.top > window.innerHeight - 30) {
            bottomCount++;
        }
    });
    
    if (topCount == 0) {
        document.getElementById("mctparent").style.opacity = 0
        document.getElementById("mctparent").style.top = "-64px"
    } else {
        document.getElementById("mctparent").style.opacity = 1
        document.getElementById("mctparent").style.top = "64px"
    }

    if (bottomCount == 0) {
        document.getElementById("mcbparent").style.opacity = 0
        document.getElementById("mcbparent").style.bottom = "-44px"
    } else {
        document.getElementById("mcbparent").style.opacity = 1
        document.getElementById("mcbparent").style.bottom = "44px"
    }
    topCountView.textContent = topCount;
    bottomCountView.textContent = bottomCount;
 }

function checkInstall(response) {
    if (response.installationStatus == false) {
        window.pywebview.api.closeApplication();
    } else {
        setTimeout(() => openWindow(), 1000);
        setTimeout(() => document.querySelector('.splashIcon').style.display = 'none', 1500);
    }
}

function openWindow(name) {
    if (name == null) { name = ".content"; }
    document.querySelector(name).style.clipPath = 'circle(75% at 50% 50%)';
    playAudio("/assets/web/fishing/sounds/guitar_out.ogg");
}

function closeWindow(name, literally) {
    if (name == null) { name = ".content"; }
    document.querySelector(name).style.clipPath = 'circle(0% at 50% 50%)';
    playAudio("/assets/web/fishing/sounds/guitar_in.ogg");
    if (literally) {
        document.querySelector('.splashIcon').style.display = 'block';
        setTimeout(() => window.pywebview.api.closeApplication(), 3000);
    }
}

function preloadAudio(files) {
    files.forEach(file => {
        const audio = new Audio(file);
        audio.preload = 'auto';
        audio.load();
        preloadedAudio[file] = audio;
        console.log(`Preloading: ${file}`);
    });
}

function playAudio(url) {
    const audio = preloadedAudio[url];
    if (audio) {
        const audioClone = audio.cloneNode();
        audioClone.play().catch(error => {
            console.error("Error playing audio:", error);
        });

        audioClone.addEventListener("ended", () => {
            audioClone.remove();
        });
    } else {
        console.warn(`Audio file ${url} is not preloaded.`);
    }
}

function changeScene(tabId) {
    const currentTab = document.querySelector('.tab.active');
    if (currentTab && currentTab.id === tabId) {
        return;
    }

    if (!sceneChanging && !settingsDisplayed) {
        
        window.pywebview.api.configure("transition").then((val) => {
            const tabs = document.querySelectorAll('.tab');
            if (val == "transition") {
                sceneChanging = true;
                closeWindow(".tabs", false);
        
                setTimeout(() => {
                    tabs.forEach(tab => {
                        tab.classList.remove('active');
                    });
        
                    document.getElementById(tabId).classList.add('active');
                    openWindow(".tabs");
                    sceneChanging = false;
                }, 1000);
            } else {
                tabs.forEach(tab => {
                    tab.classList.remove('active');
                });
        
                document.getElementById(tabId).classList.add('active');
            }

        });
    }
}

function addSoundEffects(element) {
    element.addEventListener('mouseover', () => playAudio("/assets/web/fishing/sounds/ui_swish.ogg"));
    element.addEventListener('mousedown', () => playAudio("/assets/web/fishing/sounds/button_down.ogg"));
    element.addEventListener('mouseup', () => playAudio("/assets/web/fishing/sounds/button_up.ogg"));
}

function mouseOverEventSound(element) {
    element.addEventListener('mouseover', () => playAudio("/assets/web/fishing/sounds/ui_swish.ogg"));
}

let settingsDisplayed = false;

function toggleSettings() {
    const settings = document.getElementById('settings');
    if (!sceneChanging && !settingsDisplayed) {
        settings.style.display = "block";
        playAudio("/assets/web/fishing/sounds/menu_blip.ogg");
        settingsDisplayed = true;
        closeWindow(".tabs", false);
        return
    } if (!sceneChanging && settingsDisplayed) {
        settings.style.display = "none";
        playAudio("/assets/web/fishing/sounds/menu_blipb.ogg");
        settingsDisplayed = false;
        openWindow(".tabs");
        return
    }
}

function switchSettingView(id) {
    const tabs = document.querySelectorAll('.settingTab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    document.getElementById(id).classList.add('active');

    const tabButtons = document.querySelectorAll('.tabButton');
    tabButtons.forEach(button => {
        button.classList.remove('active');
    });

    const activeTabButton = document.querySelector(`.tabButton[data-tab="${id}"]`);
    if (activeTabButton) {
        activeTabButton.classList.add('active');
    }
}

function notify(message, duration = 3000) {
    const toast = document.createElement("div");
    toast.classList.add("toast");
    toast.textContent = message;

    const container = document.getElementById("toast-container");
    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("show")
        playAudio("/assets/web/fishing/sounds/notification.ogg")
    }, 50);

    setTimeout(() => {
        toast.classList.remove("show");
        toast.classList.add("hide");
        
        setTimeout(() => container.removeChild(toast), 500);
    }, duration);
}

function scriptsReady() {
    setInterval(() => {
        function changeState(response) {
            const isRunning = response.running;
            if (isRunning !== previousIsRunning) {
                previousIsRunning = isRunning;

                if (isRunning === false) {
                    document.querySelector(".run").style.opacity = '1';
                    document.querySelector(".run").style.pointerEvents = 'all';
                } else {
                    document.querySelector(".run").style.opacity = '0';
                    document.querySelector(".run").style.pointerEvents = 'none';
                }
            }
        }

        window.pywebview.api.webfishingRunning().then(changeState);
    }, 500);

    const audioFiles = [
        '/assets/web/fishing/sounds/guitar_out.ogg',
        '/assets/web/fishing/sounds/guitar_in.ogg',
        '/assets/web/fishing/sounds/ui_swish.ogg',
        '/assets/web/fishing/sounds/button_down.ogg',
        '/assets/web/fishing/sounds/button_up.ogg',
        '/assets/web/fishing/sounds/menu_blip.ogg',
        '/assets/web/fishing/sounds/menu_blipb.ogg',
        '/assets/web/fishing/sounds/zip.ogg',
        '/assets/web/fishing/sounds/notification.ogg',
    ];
    preloadAudio(audioFiles);

    window.pywebview.api.isInstalled().then(checkInstall);
    document.querySelectorAll('button').forEach(addSoundEffects);
    document.querySelectorAll('.tabButton').forEach(addSoundEffects);
    document.querySelectorAll(".dropdown-header").forEach(mouseOverEventSound);

    const scrollElement = document.querySelector('#Mods');
    const audio = document.getElementById('audio');

    if (scrollElement && audio) {
      let isScrolling = false;

      scrollElement.addEventListener('scroll', function() {
        window.pywebview.api.configure("reelsound").then((val) => {
            if (val == "reel") {
                if (!isScrolling) {
                    isScrolling = true;
                    audio.play();
                }
        
                clearTimeout(scrollElement.scrollTimeout);
        
                scrollElement.scrollTimeout = setTimeout(function() {
                    isScrolling = false;
                    audio.pause();
                    audio.currentTime = 0;
                }, 50);
            }
        });
      });
    }

    // configs
    window.pywebview.api.configure("hlsmods").then((val) => {
        setDropdownValue("hlsmods", val === "findhls" ? "findhls" : "nofindhls")
    })

    window.pywebview.api.configure("debugging").then((val) => {
        setDropdownValue("debugging", val === "debena" ? "debena" : "debdis")
    })

    window.pywebview.api.configure("filter").then((val) => {
        setDropdownValue("filter", val)
    })

    window.pywebview.api.configure("category").then((val) => {
        setDropdownValue("category", val)
    })

    window.pywebview.api.configure("nsfw").then((val) => {
        setDropdownValue("nsfw", val)
    })

    document.getElementById('searchInput').addEventListener('input', handleChange);
        
    window.pywebview.api.getModList().then(handleChange)
    updateModsCount()
};
