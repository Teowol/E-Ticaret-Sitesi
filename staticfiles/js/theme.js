(function () {
    const savedTheme = localStorage.getItem("theme") || "light";
    document.documentElement.setAttribute("data-theme", savedTheme);
})();

document.addEventListener("DOMContentLoaded", function () {
    const themeButton = document.getElementById("themeToggle");

    function updateThemeButton() {
        const theme = document.documentElement.getAttribute("data-theme");
        const icon = themeButton.querySelector("i");
        const text = themeButton.querySelector("span");

        if (theme === "dark") {
            icon.className = "bi bi-sun-fill";
            text.textContent = " Açık";
        } else {
            icon.className = "bi bi-moon-fill";
            text.textContent = " Koyu";
        }
    }

    updateThemeButton();

    themeButton.addEventListener("click", function () {
        const currentTheme =
            document.documentElement.getAttribute("data-theme");

        const newTheme = currentTheme === "dark" ? "light" : "dark";

        document.documentElement.setAttribute("data-theme", newTheme);
        localStorage.setItem("theme", newTheme);

        updateThemeButton();
    });
});
