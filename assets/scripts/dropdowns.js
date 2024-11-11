const dropdowns = document.querySelectorAll('.custom-dropdown');

dropdowns.forEach(dropdown => {
    const dropdownHeader = dropdown.querySelector('.dropdown-header');
    const options = dropdown.querySelectorAll('.option');
    const selectedOption = dropdown.querySelector('.selected-option');

    let dropdownValue = "";
    const dropdownName = dropdown.getAttribute('data-name');

    dropdownHeader.addEventListener('click', () => {
        dropdown.classList.toggle('open');
    });

    options.forEach(option => {
        option.addEventListener('click', () => {
            selectedOption.textContent = option.textContent;
            options.forEach(opt => opt.classList.remove('selected'));
            option.classList.add('selected');
            dropdown.classList.remove('open');
            dropdownValue = option.getAttribute('data-value');
            console.log(`${dropdownName} selected value:`, dropdownValue);
            handleChange(dropdownName, dropdownValue);
            window.pywebview.api.configure(dropdownName, dropdownValue);
        });
    });
});

function getValue(name) {
    const dropdown = document.querySelector(`.custom-dropdown[data-name="${name}"]`);
    if (dropdown) {
        const selectedOption = dropdown.querySelector('.option.selected');
        return selectedOption ? selectedOption.getAttribute('data-value') : null;
    }
    return null;
}

function setDropdownValue(name, value) {
    const dropdown = document.querySelector(`.custom-dropdown[data-name="${name}"]`);
    if (dropdown) {
        const options = dropdown.querySelectorAll('.option');
        const selectedOption = dropdown.querySelector('.selected-option');
        const optionToSelect = Array.from(options).find(option => option.getAttribute('data-value') === value);

        if (optionToSelect) {
            selectedOption.textContent = optionToSelect.textContent;
            options.forEach(opt => opt.classList.remove('selected'));
            optionToSelect.classList.add('selected');
            console.log(`${name} updated to value: ${value}`);
        }
    }
}
