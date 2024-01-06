/* Filter Price */
const chevronDownPrice = document.querySelector(".chevron-down-price");
const chevronUpPrice = document.querySelector(".chevron-up-price");
const filterPrice = document.querySelector(".filter-price");

chevronDownPrice.addEventListener("click",function(){
    filterPrice.classList.add("active");
    chevronDownPrice.style.display = "none";
    chevronUpPrice.style.display = "block";
})

chevronUpPrice.addEventListener("click",function(){
    filterPrice.classList.remove("active");
    chevronUpPrice.style.display = "none";
    chevronDownPrice.style.display = "block";
})

/* Filter Type */
const chevronDownType = document.querySelector(".chevron-down-type");
const chevronUpType = document.querySelector(".chevron-up-type");
const filterType = document.querySelector(".filter-type");

chevronDownType.addEventListener("click",function(){
    filterType.classList.add("active");
    chevronDownType.style.display = "none";
    chevronUpType.style.display = "block";
})

chevronUpType.addEventListener("click",function(){
    filterType.classList.remove("active");
    chevronUpType.style.display = "none";
    chevronDownType.style.display = "block";
})

/* Filter Name */
const chevronDownName = document.querySelector(".chevron-down-name");
const chevronUpName = document.querySelector(".chevron-up-name");
const filterName = document.querySelector(".filter-name");

chevronDownName.addEventListener("click",function(){
    filterName.classList.add("active");
    chevronDownName.style.display = "none";
    chevronUpName.style.display = "block";
})

chevronUpName.addEventListener("click",function(){
    filterName.classList.remove("active");
    chevronUpName.style.display = "none";
    chevronDownName.style.display = "block";
})

/* Cart */
const openShopping = document.querySelector(".cart-medicine__shopping");
const closeShopping = document.querySelector(".closeShopping");
const list = document.querySelector(".cart-list");
const listCard = document.querySelector(".listCard");
const body = document.querySelector("body");
const total = document.querySelector(".total");
const quantity = document.querySelector(".cart-medicine__shopping--quantity");

openShopping.addEventListener("click", function(){
    body.classList.add("active");
})

