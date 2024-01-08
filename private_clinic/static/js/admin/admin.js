
const darkMode = document.querySelector('.dark-mode');

darkMode.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode-variables');
    darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
    darkMode.querySelector('span:nth-child(2)').classList.toggle('active');
})

//Table choosing in analytics.html
const salesBtn = document.querySelector(".salesBtn");
const medicineBtn = document.querySelector(".medicineBtn");
const salesChart = document.querySelector(".sales__chart");
const medicineChart = document.querySelector(".medicine__chart");
const salesTable = document.querySelector(".sales__table");
const medicineTable = document.querySelector(".medicine__table");

salesBtn.addEventListener('click', function (){
    salesBtn.classList.add("is__choose");
    salesChart.style.display = "block";
    salesTable.style.display = "block";
    medicineChart.style.display = "none";
    medicineTable.style.display = "none";
    medicineBtn.classList.remove("is__choose");
})

medicineBtn.addEventListener('click', function (){
    salesBtn.classList.remove("is__choose");
    salesChart.style.display = "none";
    salesTable.style.display = "none";
    medicineChart.style.display = "block";
    medicineTable.style.display = "block";
    medicineBtn.classList.add("is__choose");
})