// Select all custom dropdowns
const dropdowns = document.querySelectorAll('.custom-dropdown');

// Iterate over each dropdown
dropdowns.forEach(dropdown => {
    const dropdownHeader = dropdown.querySelector('.dropdown-header');
    const options = dropdown.querySelectorAll('.option');
    const selectedOption = dropdown.querySelector('.selected-option');

    let dropdownValue = ""; // default filter value for each dropdown
    const dropdownName = dropdown.getAttribute('data-name'); // Get the unique name for each dropdown

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
        });
    });
});

// Function to get the selected value (data-value) of a specific dropdown by its name
function getValue(name) {
    const dropdown = document.querySelector(`.custom-dropdown[data-name="${name}"]`);
    if (dropdown) {
        const selectedOption = dropdown.querySelector('.option.selected');
        return selectedOption ? selectedOption.getAttribute('data-value') : null;
    }
    return null;
}