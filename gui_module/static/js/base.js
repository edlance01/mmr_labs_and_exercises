
    const logo = document.getElementById("logo");
    const popupMenu = document.getElementById("popup-menu");
    const clearHistoryBtn = document.getElementById("clear-history-btn");

    // Toggle dropdown menu visibility
    logo.addEventListener('click', function (event) {
        event.stopPropagation(); // Prevent click event from bubbling
        popupMenu.style.display = popupMenu.style.display === 'block' ? 'none' : 'block';

        // Position the dropdown menu to the right of the logo
        popupMenu.style.left = `${logo.getBoundingClientRect().right + window.scrollX}px`; // Align to the right of the logo
        popupMenu.style.top = `${logo.getBoundingClientRect().top + window.scrollY}px`; // Position at the top of the logo
    });

    // Handle clear history button
    clearHistoryBtn.addEventListener("click", function () {
        fetch("/clear_history", { method: "POST" })
            .then((response) => {
                if (response.ok) {
                    location.reload(); // Reload the page after clearing
                }
            });
    });

    // Hide the menu when clicking outside
    document.addEventListener("click", function (event) {
        if (!popupMenu.contains(event.target) && event.target !== logo) {
            popupMenu.style.display = "none"; // Hide menu when clicking outside
        }
    });

