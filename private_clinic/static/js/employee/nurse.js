const manageBtn = document.querySelector("#manage-btn");
const examinationBtn = document.querySelector("#examination-btn");
const tableManage = document.querySelector(".table-manage");
const tableManageTitle = document.querySelector(".manage-title");
const tableEx = document.querySelector(".table-examination");
const tableExTitle = document.querySelector(".examination-title");
const exBtn = document.querySelector(".ex-btn");
manageBtn.addEventListener("click", function (event) {
    manageBtn.classList.add("active");
    tableManageTitle.style.display = "block";
    tableManage.style.display = "flex";
    tableManage.style.justifyContent = "center";
    tableManage.style.alignItems = "center";
    tableExTitle.style.display = "none";
    tableEx.style.display = "none";
    exBtn.style.display = "none";
    examinationBtn.classList.remove("active");
})

examinationBtn.addEventListener("click", function (event) {
    examinationBtn.classList.add("active");
    tableExTitle.style.display = "block";
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