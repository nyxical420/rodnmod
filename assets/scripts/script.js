let sceneChanging = false;
let previousIsRunning = null;

function showResponse(response) {
    var container = document.getElementById('res')
    container.textContent = response
    container.style.display = 'block'
}

function checkInstall(response) {
    if (response.installationStatus == false) {
        alert("WEBweb/fishing Installation not found.\nPlease make sure you have WEBweb/fishing installed on Steam!")
        window.pywebview.api.closeApplication()
    } else {
        setTimeout(() => openWindow(), 1000);
        setTimeout(() => document.querySelector('.splashIcon').style.display = 'none', 1500);
    }
}

function openWindow(name) {
    if (name == null) { name = ".content" }
    document.querySelector(name).style.clipPath = 'circle(73% at 50% 50%)';
    playAudio("/assets/web/fishing/sounds/guitar_out.ogg");
}

function closeWindow(name, literally) {
    if (name == null) { name = ".content" }
    document.querySelector(name).style.clipPath = 'circle(0% at 50% 50%)';
    playAudio("/assets/web/fishing/sounds/guitar_in.ogg");
    if (literally) {
        document.querySelector('.splashIcon').style.display = 'block'
        setTimeout(() => window.pywebview.api.closeApplication(), 3000);
        //setTimeout(() => playAudio('/assets/web/get.mp3'), 2700);
    }
}

function playAudio(url) {
    const audio = new Audio(url);
    audio.play().catch(error => {
        console.error("Error playing audio:", error);
    });
    audio.addEventListener("ended", () => {
        audio.remove();
    });
}


function changeScene(tabId) {
    const currentTab = document.querySelector('.tab.active');
    if (currentTab && currentTab.id === tabId) {
        return;
    }
    
    if (sceneChanging == false) {
        sceneChanging = true
        closeWindow(".tabs", false)
        
        setTimeout(() => {
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => {
                tab.classList.remove('active');
            });
            
            document.getElementById(tabId).classList.add('active');
            openWindow(".tabs")
            sceneChanging = false
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

    setTimeout(() => window.pywebview.api.getModList(), 50);
    setTimeout(() => window.pywebview.api.isInstalled().then(checkInstall), 50);
    document.querySelectorAll('button').forEach(addSoundEffects);
    document.querySelector(".dropdown-header").addEventListener('mouseover', () => playAudio("/assets/web/fishing/sounds/ui_swish.ogg"));;
    document.body.style.zoom = '0.8';

    
});