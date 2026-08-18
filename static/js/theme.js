(function () {
    const savedTheme = localStorage.getItem("computersensei-theme") || "light";
    document.documentElement.setAttribute("data-theme", savedTheme);
})();

document.addEventListener("DOMContentLoaded", function () {
    const lightButton = document.getElementById("themeLightBtn");
    const darkButton = document.getElementById("themeDarkBtn");
    const lightCheck = document.querySelector(".theme-check-light");
    const darkCheck = document.querySelector(".theme-check-dark");

    function updateThemeButtons() {
        const currentTheme = document.documentElement.getAttribute("data-theme");

        if (currentTheme === "dark") {
            lightButton?.classList.remove("active");
            darkButton?.classList.add("active");
            lightCheck?.classList.add("d-none");
            darkCheck?.classList.remove("d-none");
        } else {
            lightButton?.classList.add("active");
            darkButton?.classList.remove("active");
            lightCheck?.classList.remove("d-none");
            darkCheck?.classList.add("d-none");
        }
    }

    function setTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("computersensei-theme", theme);
        updateThemeButtons();
    }

    lightButton?.addEventListener("click", function () {
        setTheme("light");
    });

    darkButton?.addEventListener("click", function () {
        setTheme("dark");
    });

    updateThemeButtons();
});