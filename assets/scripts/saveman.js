async function generateSaveItems() {
    const savesListContainer = document.querySelector('.savesList');
    savesListContainer.innerHTML = '';

    try {
        const saveData = await window.pywebview.api.getSavesList();

        const fragment = document.createDocumentFragment();

        saveData.forEach(save => {
            const saveItem = document.createElement('div');
            saveItem.classList.add('saveItem');
            saveItem.style.cssText = `
                color: #5a755a; font-size: 24px; gap: 5px;
                display: grid; grid-template-columns: 1fr auto auto;
                background-color: #ffeed5; border-radius: 15px;
                box-shadow: 0 4px 0 #6a4420; padding: 5px;
                height: auto; width: 100%;
            `;

            // Save filename text
            const fileNameText = document.createElement('text');
            fileNameText.textContent = save.filename;
            fileNameText.style.cssText = 'margin: auto auto auto 5px;';
            saveItem.appendChild(fileNameText);

            // Save creation time
            const creationTime = document.createElement('div');
            creationTime.innerHTML = `<text>${save.creationTime}</text>`;
            saveItem.appendChild(creationTime);

            // Buttons container
            const buttonContainer = document.createElement('div');
            buttonContainer.style.cssText = 'margin-left: auto; gap: 5px; display: flex;';

            // Delete button
            const deleteButton = document.createElement('button');
            deleteButton.type = 'normalButton';
            deleteButton.style.cssText = 'width: 100px; height: 30px;';
            deleteButton.innerHTML = '<text style="pointer-events: none;">Delete</text>';
            deleteButton.onmouseup = () => {
                window.pywebview.api.deleteSave(save.filename);
            };
            buttonContainer.appendChild(deleteButton);

            // Load button
            const loadButton = document.createElement('button');
            loadButton.type = 'normalButton';
            loadButton.style.cssText = 'width: 150px; height: 30px;';
            loadButton.innerHTML = '<text style="pointer-events: none;">Load</text>';
            loadButton.onmouseup = () => {
                window.pywebview.api.loadSave(save.filename);
            };
            buttonContainer.appendChild(loadButton);

            saveItem.appendChild(buttonContainer);
            fragment.appendChild(saveItem);
        });

        savesListContainer.appendChild(fragment);
    } catch (error) {
        console.error('Failed to fetch saves:', error);
        savesListContainer.textContent = 'Failed to load saves.';
    }
}
