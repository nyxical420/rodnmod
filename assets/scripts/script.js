document.body.style.zoom = '1';

let sceneChanging = false;
let previousIsRunning = null;
const preloadedAudio = {};

function showResponse(response) {
    var container = document.getElementById('res');
    container.textContent = response;
    container.style.display = 'block';
}

let previousTopCount = 0;
let previousBottomCount = 0;

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

    const topCountElement = document.getElementById("mctparent");
    const bottomCountElement = document.getElementById("mcbparent");

    if (topCount === 0) {
        topCountElement.style.opacity = 0;
        topCountElement.style.top = "-64px";
    } else {
        topCountElement.style.opacity = 1;
        topCountElement.style.top = "64px";

        if (topCount !== previousTopCount) {
            topCountElement.style.backgroundColor = "#9c914a";
            setTimeout(() => {
                topCountElement.style.backgroundColor = "#5a755a";
            }, 300);
        }
    }

    if (bottomCount === 0) {
        bottomCountElement.style.opacity = 0;
        bottomCountElement.style.bottom = "-44px";
    } else {
        bottomCountElement.style.opacity = 1;
        bottomCountElement.style.bottom = "44px";

        if (bottomCount !== previousBottomCount) {
            bottomCountElement.style.backgroundColor = "#9c914a";
            setTimeout(() => {
                bottomCountElement.style.backgroundColor = "#5a755a";
            }, 300);
        }
    }

    topCountView.textContent = topCount;
    bottomCountView.textContent = bottomCount;

    previousTopCount = topCount;
    previousBottomCount = bottomCount;
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
        console.warn(`Audio file ${url} is not preloaded. Preloading now...`);
        preloadAudio(url);
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
    const menu = document.getElementById('menuCt');
    if (!sceneChanging && !settingsDisplayed) {
        settings.style.display = "block";
        menu.style.opacity = '0'; 
        menu.style.pointerEvents = 'none';
        playAudio("/assets/web/fishing/sounds/menu_blip.ogg");
        settingsDisplayed = true;
        closeWindow(".tabs", false);
        return
    } if (!sceneChanging && settingsDisplayed) {
        settings.style.display = "none";
        menu.style.opacity = '1'; 
        menu.style.pointerEvents = 'auto';
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

    document.querySelectorAll('button').forEach(addSoundEffects);
    document.querySelectorAll('.tabButton').forEach(addSoundEffects);
    document.querySelectorAll(".dropdown-header").forEach(mouseOverEventSound);

    const scrollElement = document.querySelector('.tabs');
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

    window.pywebview.api.getPathOverride().then((val) => {
        document.getElementById('pathOverride').value = val
    })

    let debounceTimer;
    document.getElementById('searchInput').addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
        }, 250);
        handleChange();
    });

    updateModsCount();
};
