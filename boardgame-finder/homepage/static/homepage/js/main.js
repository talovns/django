// Текущий год в подвале страницы
const yearElement = document.getElementById("current-year");
if (yearElement) {
    yearElement.textContent = new Date().getFullYear();
}

// Подсветка пункта меню текущего раздела
const currentPath = window.location.pathname;
document.querySelectorAll(".site-nav .nav-link").forEach((link) => {
    const linkPath = new URL(link.href).pathname;
    const isHome = linkPath === "/";
    if ((isHome && currentPath === "/") || (!isHome && currentPath.startsWith(linkPath))) {
        link.classList.add("active");
    }
});
