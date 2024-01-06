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