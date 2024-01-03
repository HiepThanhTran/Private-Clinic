/* Header */
const nav = document.querySelector("header .my-nav");
window.addEventListener("scroll", function () {
    if (window.scrollY > 600) {
        nav.classList.add("active");
    }
    else {
        nav.classList.remove("active");
    }
})

/* Header Mobile */
const btnOpenMain = document.querySelector(".btn-open");
const btnClose = document.querySelector(".nav__menu .btn-close");
const menu = document.querySelector(".nav__menu");

btnOpenMain.addEventListener("click", function () {
    menu.classList.add("hidden");
})

btnClose.addEventListener("click", function () {
    menu.classList.remove("hidden");
})