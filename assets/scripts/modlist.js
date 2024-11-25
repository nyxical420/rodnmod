let isUpdating = false;
let nsfwToggled = true;
let configNsfw = "hidensfw";

function handleChange() {
    if (isUpdating) return;
    isUpdating = true;

    const scrollElement = document.getElementById('Mods');
    const scrollPosition = scrollElement.scrollTop;

    let searchValue = document.getElementById('searchInput').value;

    window.pywebview.api.searchModList(searchValue, getValue("filter"), getValue("category"), getValue("nsfw"))
        .then(generateModItems)
        .finally(() => {
            window.requestAnimationFrame(() => {
                scrollElement.scrollTop = scrollPosition;
            });
            isUpdating = false;
        });
}

const ignoreList = [
    "Hook_Line_and_Sinker",
    "GDWeave",
    "r2modman",
    "GaleModManager",
    "HLSReborn"
];

function generateModItems(modData) {
    const modItemsContainer = document.querySelector('.modItems');
    const fragment = document.createDocumentFragment();
    console.log(modData);

    Object.keys(modData).forEach(modKey => {
        const mod = modData[modKey];

        if (ignoreList.includes(mod.modName)) {
            return
        }
        
        if (mod.isNSFW && getValue("nsfw") == "hidensfw") {
            return
        }

        // Create the main item container
        const itemDiv = document.createElement('div');
        itemDiv.className = 'item';
        itemDiv.style = "display: grid; grid-template-columns: auto 1fr; gap: 5px; width: 100%; height: 150px; margin-bottom: 25px;";

        // Create the mod icon image
        const imageContainer = document.createElement('div');
        imageContainer.style.position = 'relative';

        const img = document.createElement('img');
        img.loading = "lazy";
        img.src = mod.versions[0].modIcon || 'assets/web/rodnmod.png';
        img.style = "image-rendering: auto; width: 150px; height: 150px; border-radius: 15px; box-shadow: 0 4px 0 #6a4420;";
        imageContainer.appendChild(img);

        if (mod.isDeprecated) {
            const deprecatedContainer = document.createElement('div');
            deprecatedContainer.style = "position: absolute; bottom: -8px; left: -14px; font-size: 18px; width: 145px; height: 30px; border-radius: 8px; padding: 5px 13px; background-color: #ffeed5; box-shadow: 0 4px 0 #6a4420; text-align: right;"
            deprecatedContainer.innerText = "DEPRECATED"
            
            const deprecatedIndicator = document.createElement('img');
            deprecatedIndicator.src = "assets/web/deprecated.png";
            deprecatedIndicator.style = "image-rendering: auto;pointer-events: none; position: absolute; top: -18px; left: 0; width: 48px; height: 48px; transform: rotate(-15deg);";
            
            deprecatedContainer.appendChild(deprecatedIndicator);
            imageContainer.appendChild(deprecatedContainer);
        }

        if (mod.isNSFW) {
            const nsfwContainer = document.createElement('div');
            nsfwContainer.style = "position: absolute; bottom: -8px; left: -14px; font-size: 18px; width: 105px; height: 30px; border-radius: 8px; padding: 5px 13px; background-color: #ffeed5; box-shadow: 0 4px 0 #6a4420; text-align: right;"
            nsfwContainer.innerText = "NSFW"
            
            const nsfwIndicator = document.createElement('img');
            nsfwIndicator.src = "assets/web/nsfw.png";
            nsfwIndicator.style = "pointer-events: none; position: absolute; top: -15px; left: 0; width: 48px; height: 48px; transform: rotate(-15deg);";
            
            nsfwContainer.appendChild(nsfwIndicator);
            imageContainer.appendChild(nsfwContainer );
        }

        itemDiv.appendChild(imageContainer);

        // Create the content container
        const contentDiv = document.createElement('div');
        contentDiv.style = "background-color: #ffeed5; border-radius: 15px; box-shadow: 0 4px 0 #6a4420; padding: 7px 10px; display: flex; flex-direction: column; height: 150px; position: relative;";
        
        // Add the updated time
        const updatedDiv = document.createElement('div');
        updatedDiv.style = "position: absolute; top: 6px; right: 10px; font-size: 16px; color: #6a4420;";
        updatedDiv.innerHTML = `
            <text style="position: relative; top: -3px">${mod.updatedAgo}</text> <img src="/assets/web/clock.png" style="image-rendering: auto; width: 16px; height: 16px;">
        `;
        contentDiv.appendChild(updatedDiv);

        const website = document.createElement('div');
        website.style = "position: absolute; top: 22px; right: 10px; font-size: 18px; color: #6a4420;";
        //website.textContent = mod.latestWebsite;
        website.innerHTML = `
           <text style="position: relative; top: -3px">${mod.latestWebsite || "No Website"}</text> <img src="/assets/web/internet.png" style="image-rendering: auto; width: 16px; height: 16px;">
        `;
        website.onmouseup = function () {
            window.pywebview.api.visitSite(mod.latestWebsite || null);
        }
        contentDiv.appendChild(website);

        // Add the title, author, and description
        const titleDiv = document.createElement('div');
        titleDiv.style = "flex: 1;";
        titleDiv.innerHTML = `
            <span style="font-size: 28px;">${mod.modName.replace(/_/g, " ")}</span>
            <span style="font-size: 20px; margin-left: 3px;">by ${mod.modAuthor}</span><br>
            <span style="font-size: 18px;">${mod.versions[0].modDescription}</span>
        `;
        contentDiv.appendChild(titleDiv);

        // Add tags
        const tagsDiv = document.createElement('div');
        tagsDiv.style = "font-size: 18px;";
        tagsDiv.innerHTML = `
            <img src="/assets/web/tag.png" style="image-rendering: auto; vertical-align: middle; width: 22px; height: 22px;"/> ${mod.modTags.join(', ')}
        `;
        contentDiv.appendChild(tagsDiv);

        // Add download count and score
        const downloadsDiv = document.createElement('div');
        downloadsDiv.style = "font-size: 18px;";
        downloadsDiv.innerHTML = `
            <img src="/assets/web/download.png" style="image-rendering: auto; vertical-align: middle; width: 22px; height: 22px;"/> ${mod.totalDownloads.toLocaleString()} 
            <img src="/assets/web/like.png" style="image-rendering: auto; vertical-align: middle; width: 22px; height: 22px;"/> ${mod.modScore.toLocaleString()}
        `;
        contentDiv.appendChild(downloadsDiv);

        // Create menu container for buttons
        const menuContainer = document.createElement('div');
        menuContainer.className = 'menuContainer';
        menuContainer.style = "background-color: transparent; display: flex; flex-direction: row; position: absolute; bottom: 45px; height: 0; overflow: visible; z-index: 0;";

        // Add buttons
        const buttonContainer = document.createElement('div');
        buttonContainer.style = "display: flex; flex-direction: row; gap: 10px; margin-left: auto; margin-right: 10px;";
        
        function addButtons(installedState) {
            buttonContainer.innerHTML = "";

            if (installedState) {
                const deleteButton = document.createElement('button');
                deleteButton.type = "menuButton";
                deleteButton.style = "display: block; --width: 135px; --height: 100px;";
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
                    async function updateMod() {
                        await window.pywebview.api.uninstallMod(`${mod.modAuthor}.${mod.modName}`);
                        addButtons(false)
                    }
                    updateMod()
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
                    async function updateMod() {
                        await window.pywebview.api.downloadMod(`${mod.modAuthor}-${mod.modName}`);
                        addButtons(true)
                    }
                    updateMod()
                };
                addSoundEffects(updateButton);
                buttonContainer.appendChild(updateButton);

            } else {
                const downloadButton = document.createElement('button');
                downloadButton.type = "menuButton";
                downloadButton.style = "display: block; --width: 150px; --height: 100px; margin-left: auto;";
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
                    async function download() {
                        await window.pywebview.api.downloadMod(`${mod.modAuthor}-${mod.modName}`);
                        addButtons(true)
                    }
                    download()
                };
                addSoundEffects(downloadButton);
                buttonContainer.appendChild(downloadButton);
            }
    
        }
        
        if (!mod.isDeprecated) {
            window.pywebview.api.uninstallMod(`${mod.modAuthor}.${mod.modName}`, true).then(addButtons);
        }


        menuContainer.appendChild(buttonContainer);
        contentDiv.appendChild(menuContainer);

        itemDiv.appendChild(contentDiv);
        fragment.appendChild(itemDiv);
    });
    
    modItemsContainer.innerHTML = '';
    modItemsContainer.appendChild(fragment)
    updateModsCount()
}