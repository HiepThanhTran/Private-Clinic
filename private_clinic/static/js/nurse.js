const manageBtn = document.querySelector("#manage-btn");
const examinationBtn = document.querySelector("#examination-btn");
const tableManage = document.querySelector(".table-manage");
const tableManageTitle = document.querySelector(".manage-title");
const tableEx = document.querySelector(".table-examination");
const tableExTitle = document.querySelector(".examination-title");
const tableM = document.querySelector(".table-manage");
const tableE = document.querySelector(".table-examination");
const exBtn = document.querySelector(".ex-btn");
manageBtn.addEventListener("click", function () {
    manageBtn.classList.add("active");
    tableManageTitle.style.display = "block";
    tableM.style.display = "flex";
    tableM.style.justifyContent = "center";
    tableM.style.alignItems = "center";
    tableExTitle.style.display = "none";
    tableEx.style.display = "none";
    exBtn.style.display = "none";
    examinationBtn.classList.remove("active");
})

examinationBtn.addEventListener("click", function () {
    examinationBtn.classList.add("active");
    tableExTitle.style.display = "block";
    tableEx.style.display = "block";
    tableEx.style.display = "flex";
    tableEx.style.justifyContent = "center";
    tableEx.style.alignItems = "center";
    tableManageTitle.style.display = "none";
    tableManage.style.display = "none";
    exBtn.style.display = "flex";
    exBtn.style.jutifyContent = "center";
    exBtn.style.alignItems = "center";
    manageBtn.classList.remove("active");
})