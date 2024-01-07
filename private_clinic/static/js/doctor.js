const manageBtn = document.querySelector("#manage-btn");
const medicalBillBtn = document.querySelector("#medical-bill-btn");
const tableManage = document.querySelector(".table-manage");
const tableManageTitle = document.querySelector(".manage-title");
const tableExaminationBill = document.querySelector(".table-examination-bill");
const tableExaminationBillTitle = document.querySelector(".examination-bill-title");
manageBtn.addEventListener("click", function (event) {
    manageBtn.classList.add("active");
    tableManageTitle.style.display = "block";
    tableManage.style.display = "flex";
    tableManage.style.justifyContent = "center";
    tableManage.style.alignItems = "center";
    tableExaminationBillTitle.style.display = "none";
    tableExaminationBill.style.display = "none";
    medicalBillBtn.classList.remove("active");
})

medicalBillBtn.addEventListener("click", function (event) {
    medicalBillBtn.classList.add("active");
    tableExaminationBillTitle.style.display = "block";
    tableExaminationBill.style.display = "flex";
    tableExaminationBill.style.justifyContent = "center";
    tableExaminationBill.style.alignItems = "center";
    tableManageTitle.style.display = "none";
    tableManage.style.display = "none";
    manageBtn.classList.remove("active");
})

const addMedicalBtn = document.querySelector(".add-medical");
const modalAddMedicine = document.querySelector(".modal-add-medicine");
const modalContainer = document.querySelector(".wrapper");
addMedicalBtn.addEventListener("click",function (event){
    event.preventDefault();
    modalAddMedicine.classList.add("open");
})

modalAddMedicine.addEventListener("click",function (){
    modalAddMedicine.classList.remove("open");
})

modalContainer.addEventListener("click",function (event){
    event.stopPropagation();
})

const addExCourseBtn = document.querySelector(".add-examination-course");
const modalAddExCourse = document.querySelector(".modal-add-examination-course");
const modalContainerExCourse = document.querySelector(".wrapper-examincation");
addExCourseBtn.addEventListener("click",function (event){
    event.preventDefault();
    modalAddExCourse.classList.add("open");
})

modalAddExCourse.addEventListener("click",function (){
    modalAddExCourse.classList.remove("open");
})

modalContainerExCourse.addEventListener("click",function (event){
    event.stopPropagation();
})
