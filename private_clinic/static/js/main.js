const showPreLoading = () => {
    const loadingModal = document.getElementById('loadingModal');
    loadingModal.style.display = 'flex';
};

const hidePreLoading = () => {
    const loadingModal = document.getElementById('loadingModal');
    loadingModal.style.display = 'none';
};

const inputTelType = document.querySelector('input[type=tel]')
const regexDigits = /\d/;

if (inputTelType) {
    inputTelType.addEventListener('keypress', (e) => {
        if (!regexDigits.test(String.fromCharCode(e.keyCode))) e.preventDefault()
    })
}

/* Back To the Top */
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