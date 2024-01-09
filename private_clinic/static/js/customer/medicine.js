/* Filter Price */
const btnDownPrice = document.querySelector(".btn-down-price");
const btnUpPrice = document.querySelector(".btn-up-price");
const filterPrice = document.querySelector(".filter-price .filter-value");
btnDownPrice.addEventListener("click", function () {
    filterPrice.classList.add("open");
    btnDownPrice.style.display = "none";
    btnUpPrice.style.display = "block";
})

btnUpPrice.addEventListener("click", function () {
    filterPrice.classList.remove("open");
    btnUpPrice.style.display = "none";
    btnDownPrice.style.display = "block";
})

/* Filter Type Medicine */
const btnDownType = document.querySelector(".btn-down-type");
const btnUpType = document.querySelector(".btn-up-type");
const filterTypeMedicine = document.querySelector(".filter-type-medicine .filter-value");
btnDownType.addEventListener("click", function () {
    filterTypeMedicine.classList.add("open");
    btnDownType.style.display = "none";
    btnUpType.style.display = "block";
})

btnUpType.addEventListener("click", function () {
    filterTypeMedicine.classList.remove("open");
    btnUpType.style.display = "none";
    btnDownType.style.display = "block";
})

/* Filter Name Medicine */
const btnDownName = document.querySelector(".btn-down-name");
const btnUpName = document.querySelector(".btn-up-name");
const filterNameMedicine = document.querySelector(".filter-name-medicine .filter-value");
btnDownName.addEventListener("click", function () {
    filterNameMedicine.classList.add("open");
    btnDownName.style.display = "none";
    btnUpName.style.display = "block";
})

btnUpName.addEventListener("click", function () {
    filterNameMedicine.classList.remove("open");
    btnUpName.style.display = "none";
    btnDownName.style.display = "block";
})

