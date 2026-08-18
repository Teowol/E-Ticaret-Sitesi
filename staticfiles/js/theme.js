// Sayfa yüklenmeden önce tema ayarını uygula (ekran yanıp sönmesini engeller)
(function () {
    const savedTheme = localStorage.getItem("theme") || "light";
    document.documentElement.setAttribute("data-theme", savedTheme);
})();

document.addEventListener("DOMContentLoaded", function () {
    const lightBtn = document.getElementById("themeLightBtn");
    const darkBtn = document.getElementById("themeDarkBtn");
    const checkLight = document.querySelector(".theme-check-light");
    const checkDark = document.querySelector(".theme-check-dark");

    function updateThemeUI() {
        const currentTheme = document.documentElement.getAttribute("data-theme") || "light";
        if (currentTheme === "dark") {
            if (checkDark) checkDark.classList.remove("d-none");
            if (checkLight) checkLight.classList.add("d-none");
            if (darkBtn) darkBtn.classList.add("active");
            if (lightBtn) lightBtn.classList.remove("active");
        } else {
            if (checkLight) checkLight.classList.remove("d-none");
            if (checkDark) checkDark.classList.add("d-none");
            if (lightBtn) lightBtn.classList.add("active");
            if (darkBtn) darkBtn.classList.remove("active");
        }
    }

    function setTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("theme", theme);
        updateThemeUI();
    }

    if (lightBtn) {
        lightBtn.addEventListener("click", function () {
            setTheme("light");
        });
    }

    if (darkBtn) {
        darkBtn.addEventListener("click", function () {
            setTheme("dark");
        });
    }

    updateThemeUI();
});