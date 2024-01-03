/* Back To Top */
const backToTopButton = document.querySelector("#back-to-top");
if (backToTopButton != null) {
    window.addEventListener("scroll", function scrollFunction() {
        if (window.scrollY > 300) {
            if (!backToTopButton.classList.contains("fadeInRight")) {
                backToTopButton.classList.remove("fadeOutRight");
                backToTopButton.classList.add("fadeInRight");
                backToTopButton.style.display = "flex";
            }
        } else {
            if (backToTopButton.classList.contains("fadeInRight")) {
                backToTopButton.classList.remove("fadeInRight");
                backToTopButton.classList.add("fadeOutRight");
                setTimeout(function () {
                    backToTopButton.style.display = "none";
                }, 250);
            }
        }
    });
    backToTopButton.addEventListener("click", function backToTop() {
        window.scrollTo(0, 0);
    });
}