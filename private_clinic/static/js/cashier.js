/* Moal Detail */
const detailBtn = document.querySelectorAll(".detail");
const modalDetail = document.querySelector(".modal-detail");
const modalDetailContainer = document.querySelector(".modal-detail table");

for (var i = 0; i < detailBtn.length; i++) {
    detailBtn[i].addEventListener("click", function () {
        modalDetail.classList.add("open");
    })
}

modalDetail.addEventListener("click", function () {
    modalDetail.classList.remove("open");
})

modalDetailContainer.addEventListener("click", function (event) {
    event.stopPropagation();
})

/* Modal Print */
const invoiceBtn = document.querySelectorAll(".invoice");
const modalPrint = document.querySelector(".modal-print");
const modalPrintContainer = document.querySelector(".modal-print table");
for (var i = 0; i < invoiceBtn.length; i++) {
    invoiceBtn[i].addEventListener("click", function () {
        modalPrint.classList.add("open");
    })
}
modalPrint.addEventListener("click", function () {
    modalPrint.classList.remove("open");
})

modalPrintContainer.addEventListener("click", function (event) {
    event.stopPropagation();
})

const manageBtn = document.querySelector("#manage-btn");
const billBtn = document.querySelector("#bill-btn");
const tableManage = document.querySelector(".table-manage");
const tableManageTitle = document.querySelector(".manage-title");
const tableBillIssued = document.querySelector(".table-bill-issued");
const tableBillIssuedTitle = document.querySelector(".bill-title");
manageBtn.addEventListener("click", function (event) {
    manageBtn.classList.add("active");
    tableManageTitle.style.display = "block";
    tableManage.style.display = "flex";
    tableManage.style.justifyContent = "center";
    tableManage.style.alignItems = "center";
    tableBillIssuedTitle.style.display = "none";
    tableBillIssued.style.display = "none";
    billBtn.classList.remove("active");
})

billBtn.addEventListener("click", function (event) {
    billBtn.classList.add("active");
    tableBillIssuedTitle.style.display = "block";
    tableBillIssued.style.display = "flex";
    tableBillIssued.style.justifyContent = "center";
    tableBillIssued.style.alignItems = "center";
    tableManageTitle.style.display = "none";
    tableManage.style.display = "none";
    manageBtn.classList.remove("active");
})