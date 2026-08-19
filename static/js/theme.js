(function () {
    const savedTheme = localStorage.getItem("computersensei-theme") || "light";
    document.documentElement.setAttribute("data-theme", savedTheme);
})();

document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("themeToggleBtn");
    const toggleText = document.getElementById("themeToggleText");

    function renderButton(theme) {
        if (!toggleText) return;

        if (theme === "dark") {
            toggleText.innerHTML =
                '<i id="themeToggleIcon" class="bi bi-moon-stars-fill text-info me-2"></i>Karanlık Tema';
        } else {
            toggleText.innerHTML =
                '<i id="themeToggleIcon" class="bi bi-sun-fill text-warning me-2"></i>Açık Tema';
        }
    }

    const currentTheme = document.documentElement.getAttribute("data-theme") || "light";
    renderButton(currentTheme);

    if (toggleBtn) {
        toggleBtn.addEventListener("click", function () {
            const current = document.documentElement.getAttribute("data-theme") || "light";
            const next = current === "dark" ? "light" : "dark";
            document.documentElement.setAttribute("data-theme", next);
            localStorage.setItem("computersensei-theme", next);
            renderButton(next);
        });
    }
});