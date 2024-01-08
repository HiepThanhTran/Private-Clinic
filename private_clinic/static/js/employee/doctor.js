const manageBtn = document.querySelector("#manage-btn");
const patientBtn = document.querySelector("#patient-btn");
const tableManage = document.querySelector(".table-manage");
const tableManageTitle = document.querySelector(".manage-title");
const tablePatient = document.querySelector(".table-patient");
const tablePatientTitle = document.querySelector(".patient-title");
manageBtn.addEventListener("click", function (event) {
    manageBtn.classList.add("active");
    tableManageTitle.style.display = "block";
    tableManage.style.display = "flex";
    tableManage.style.justifyContent = "center";
    tableManage.style.alignItems = "center";
    tablePatientTitle.style.display = "none";
    tablePatient.style.display = "none";
    patientBtn.classList.remove("active");
})

patientBtn.addEventListener("click", function (event) {
    patientBtn.classList.add("active");
    tablePatientTitle.style.display = "block";
    tablePatient.style.display = "flex";
    tablePatient.style.justifyContent = "center";
    tablePatient.style.alignItems = "center";
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

const invoiceBtn = document.querySelectorAll("button.invoice");
const modalCreateMedicalBill = document.querySelector(".modal-create-medical-bill");
const modalContainerCreateMedicalBill = document.querySelector(".modal-create-medical-bill table")
for(var i=0;i<invoiceBtn.length;i++)
{
    invoiceBtn[i].addEventListener("click",function (){
       modalCreateMedicalBill.classList.add("open");
    })
}

modalCreateMedicalBill.addEventListener("click",function (){
    modalCreateMedicalBill.classList.remove("open");
})

modalContainerCreateMedicalBill.addEventListener("click",function (e){
    e.stopPropagation();
})

