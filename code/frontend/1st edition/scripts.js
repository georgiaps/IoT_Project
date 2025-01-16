document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll("nav a");
    const sections = document.querySelectorAll(".tab-content");

    tabs.forEach(tab => {
        tab.addEventListener("click", event => {
            event.preventDefault(); // Prevent default link behavior

            // Hide all sections
            sections.forEach(section => section.style.display = "none");

            // Show the clicked section
            const targetId = tab.getAttribute("href").substring(1); // Get target ID without the '#'
            document.getElementById(targetId).style.display = "block";
        });
    });
});
