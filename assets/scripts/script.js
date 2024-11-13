document.body.style.zoom = '0.8';

let sceneChanging = false;
let previousIsRunning = null;
const preloadedAudio = {};  // Store preloaded audio objects

function showResponse(response) {
    var container = document.getElementById('res');
    container.textContent = response;
    container.style.display = 'block';
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
    document.querySelector(name).style.clipPath = 'circle(73% at 50% 50%)';
    playAudio("/assets/web/fishing/sounds/guitar_out.ogg");
}

function closeWindow(name, literally) {
    if (name == null) { name = ".content"; }
    document.querySelector(name).style.clipPath = 'circle(0% at 50% 50%)';
    playAudio("/assets/web/fishing/sounds/guitar_in.ogg");
    if (literally) {
        document.querySelector('.splashIcon').style.display = 'block';
        setTimeout(() => window.pywebview.api.closeApplication(), 3000);
        //setTimeout(() => playAudio('/assets/web/get.mp3'), 2700);
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
        sceneChanging = true;
        closeWindow(".tabs", false);

        setTimeout(() => {
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => {
                tab.classList.remove('active');
            });

            document.getElementById(tabId).classList.add('active');
            openWindow(".tabs");
            sceneChanging = false;
        }, 1000);
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

document.addEventListener('DOMContentLoaded', function () {
    function checkPywebviewApi() {
        if (typeof window.pywebview === 'undefined' || typeof window.pywebview.api === 'undefined') {
            console.warn("pywebview.api is not available. Refreshing page...");
            location.reload();
        }
    }

    checkPywebviewApi();

    let isDragging = false;
    let startX, startY, offsetX, offsetY;
    const movementThreshold = 0;

    const titleBar = document.querySelector('.titleBar');

    titleBar.addEventListener('mousedown', (e) => {
        isDragging = true;
        startX = e.clientX;
        startY = e.clientY;
        offsetX = e.clientX - titleBar.getBoundingClientRect().left;
        offsetY = e.clientY - titleBar.getBoundingClientRect().top;
    });

    document.addEventListener('mousemove', (e) => {
        if (isDragging) {
            const dx = Math.abs(e.clientX - startX);
            const dy = Math.abs(e.clientY - startY);

            if (dx > movementThreshold || dy > movementThreshold) {
                const x = e.clientX - offsetX;
                const y = e.clientY - offsetY;
                window.pywebview.api.dragWindow(x, y);
                startX = e.clientX;
                startY = e.clientY;
            }
        }
    });

    document.addEventListener('mouseup', () => {
        if (isDragging) {
            isDragging = false;
        }
    });

    document.addEventListener('mouseleave', () => {
        if (isDragging) {
            isDragging = false;
        }
    });

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
});
