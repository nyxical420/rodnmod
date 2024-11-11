let isUpdating = false;
let nsfwToggled = true;
let showNSFW = false;

function handleChange() {
    if (isUpdating) return;
    isUpdating = true;

    let searchValue = document.getElementById('searchInput').value;

    window.pywebview.api.searchModList(searchValue, getValue("filter"), getValue("category"), showNSFW)
        .then(generateModItems)
        .finally(() => isUpdating = false);
}

function toggleNSFW() {
    let text = document.getElementById('nsfwText');
    let image = document.getElementById('nsfwImage');

    if (nsfwToggled) {
        text.innerText = "Hide NSFW"
        image.src = "/assets/web/nsfw.png"
        nsfwToggled = false;
        showNSFW = true;
        playAudio("/assets/web/fishing/sounds/zip.ogg")
    } else {
        text.innerText = "Show NSFW";
        image.src = "/assets/web/normal.png";
        nsfwToggled = true;
        showNSFW = false;
    }

    handleChange()
}

const ignoreList = [
    "Hook_Line_and_Sinker",
    "GDWeave",
];

function generateModItems(modData) {
    const modItemsContainer = document.querySelector('.modItems');
    modItemsContainer.innerHTML = '';
    console.log(modData);
    
    Object.keys(modData).forEach(modKey => {
        const mod = modData[modKey];

        if (ignoreList.includes(mod.modName) || mod.isDeprecated) {
            return;
        }
        
        // Create the main item container
        const itemDiv = document.createElement('div');
        itemDiv.className = 'item';
        itemDiv.style = "display: grid; grid-template-columns: auto 1fr; gap: 5px; width: 100%; height: 150px; margin-bottom: 25px;";

        // Create the mod icon image
        const img = document.createElement('img');
        img.src = mod.versions[0].modIcon || 'https://placehold.co/150';
        img.style = "width: 150px; height: 150px; border-radius: 15px; box-shadow: 0 4px 0 #6a4420;";
        img.laz
        itemDiv.appendChild(img);

        // Create the content container
        const contentDiv = document.createElement('div');
        contentDiv.style = "background-color: #ffeed5; border-radius: 15px; box-shadow: 0 4px 0 #6a4420; padding: 10px; display: flex; flex-direction: column; height: 100%; position: relative;";
        
        // Add the updated time
        const updatedDiv = document.createElement('div');
        updatedDiv.style = "position: absolute; top: 8px; right: 10px; font-size: 16px; color: #6a4420;";
        updatedDiv.textContent = mod.updatedAgo;
        contentDiv.appendChild(updatedDiv);

        const website = document.createElement('div');
        website.style = "position: absolute; top: 22px; right: 10px; font-size: 16px; color: #6a4420;";
        website.textContent = mod.latestWebsite;
        website.onmouseup = function () {
            window.pywebview.api.visitSite(mod.latestWebsite);
        }
        contentDiv.appendChild(website);

        // Add the title, author, and description
        const titleDiv = document.createElement('div');
        titleDiv.style = "flex: 1;";
        titleDiv.innerHTML = `
            <span style="font-size: 28px;">${mod.modName.replace(/_/g, " ")}</span>
            <span style="font-size: 22px; margin-left: 3px;">by ${mod.modAuthor}</span><br>
            <span style="font-size: 20px;">${mod.versions[0].modDescription}</span>
        `;
        contentDiv.appendChild(titleDiv);

        // Add tags
        const tagsDiv = document.createElement('div');
        tagsDiv.style = "font-size: 18px;";
        tagsDiv.innerHTML = `
            <img src="/assets/web/tag.png" style="vertical-align: middle; width: 22px; height: 22px;"/> ${mod.modTags.join(', ')}
        `;
        contentDiv.appendChild(tagsDiv);

        // Add download count and score
        const downloadsDiv = document.createElement('div');
        downloadsDiv.style = "font-size: 18px;";
        downloadsDiv.innerHTML = `
            <img src="/assets/web/download.png" style="vertical-align: middle; width: 22px; height: 22px;"/> ${mod.totalDownloads.toLocaleString()} 
            <img src="/assets/web/like.png" style="vertical-align: middle; width: 22px; height: 22px;"/> ${mod.modScore.toLocaleString()}
        `;
        contentDiv.appendChild(downloadsDiv);

        // Create menu container for buttons
        const menuContainer = document.createElement('div');
        menuContainer.className = 'menuContainer';
        menuContainer.style = "background-color: transparent; display: flex; flex-direction: row; position: absolute; bottom: 45px; height: 0; overflow: visible;";

        // Add buttons
        const buttonContainer = document.createElement('div');
        buttonContainer.style = "display: flex; flex-direction: row; gap: 10px; margin-left: auto; margin-right: 10px;";
        
        function addButtons(installedState) {
            if (installedState) {
                const deleteButton = document.createElement('button');
                deleteButton.type = "menuButton";
                deleteButton.style = "display: block; --width: 120px; --height: 100px;";
                deleteButton.innerHTML = `
                    <div style="pointer-events: none; animation: none;" class="floatingIcon">
                        <img src="/assets/web/trash.png" class="spinning-image">
                    </div>
                    <text id="${mod.modName}-deleteButton" style="pointer-events: none;">Delete Mod</text>
                `;
                deleteButton.onmouseup = function() {
                    const delText = document.getElementById(`${mod.modName}-deleteButton`);

                    delText.innerText = "Deleting...";
                    deleteButton.onmouseup = "";
                    window.pywebview.api.uninstallMod(`${mod.modAuthor}.${mod.modName}`).then(handleChange);
                };
                addSoundEffects(deleteButton);
                buttonContainer.appendChild(deleteButton);

                const updateButton = document.createElement('button');
                updateButton.type = "menuButton";
                updateButton.style = "display: block; --width: 150px; --height: 100px; margin-left: auto;";
                updateButton.innerHTML = `
                    <div style="pointer-events: none; animation: none;" class="floatingIcon">
                        <img src="/assets/web/download_tacklebox.png" class="spinning-image">
                    </div>
                    <text id="${mod.modName}-updateButton" style="pointer-events: none;">Update Mod</text>
                `;
                updateButton.onmouseup = function() {
                    const downText = document.getElementById(`${mod.modName}-updateButton`);

                    downText.innerText = "Updating...";
                    updateButton.onmouseup = "";
                    window.pywebview.api.downloadMod(`${mod.modAuthor}-${mod.modName}`).then(handleChange);
                };
                addSoundEffects(updateButton);
                buttonContainer.appendChild(updateButton);

            } else {
                const downloadButton = document.createElement('button');
                downloadButton.type = "menuButton";
                downloadButton.style = "display: block; --width: 135px; --height: 100px; margin-left: auto;";
                downloadButton.innerHTML = `
                    <div style="pointer-events: none; animation: none;" class="floatingIcon">
                        <img src="/assets/web/download_tacklebox.png" class="spinning-image">
                    </div>
                    <text id="${mod.modName}-downloadButton" style="pointer-events: none;">Download Mod</text>
                `;
                downloadButton.onmouseup = function() {
                    const downText = document.getElementById(`${mod.modName}-downloadButton`);

                    downText.innerText = "Downloading...";
                    downloadButton.onmouseup = "";
                    window.pywebview.api.downloadMod(`${mod.modAuthor}-${mod.modName}`).then(handleChange);
                };
                addSoundEffects(downloadButton);
                buttonContainer.appendChild(downloadButton);
            }
    
        }
        
        window.pywebview.api.uninstallMod(`${mod.modAuthor}.${mod.modName}`, true).then(addButtons);


        menuContainer.appendChild(buttonContainer);
        contentDiv.appendChild(menuContainer);

        itemDiv.appendChild(contentDiv);
        modItemsContainer.appendChild(itemDiv);

    });
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('searchInput').addEventListener('input', handleChange);
    //document.getElementById('filterSelect').addEventListener('change', handleChange);
        
    setTimeout(() => window.pywebview.api.getModList().then(generateModItems), 50);
    setTimeout(() => handleChange(), 50);
});
