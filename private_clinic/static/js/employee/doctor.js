let medicines_list = {}
let packages_list = {}
window.onload = () => {
    fetch('/api/employee/doctor/load-medicine', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    }).then(response => response.json())
        .then(data => {
            medicines_list = data
        })
        .catch(error => {
            console.log(error)
        })

    fetch('/api/employee/doctor/load-packages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    }).then(response => response.json())
        .then(data => {
            packages_list = data
        })
        .catch(error => {
            console.log(error)
        })
}

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

const addMedicineBtn = document.querySelector(".add-medicine");
const modalAddMedicine = document.querySelector(".modal-add-medicine");
const modalContainer = document.querySelector(".wrapper");

addMedicineBtn.addEventListener("click", function (event) {
    event.preventDefault();
    modalAddMedicine.classList.add("open");
})

modalAddMedicine.addEventListener("click", function () {
    modalAddMedicine.classList.remove("open");
})

modalContainer.addEventListener("click", function (event) {
    event.stopPropagation();
})

const addExCourseBtn = document.querySelector(".add-examination-packages");
const modalAddExCourse = document.querySelector(".modal-add-examination-packages");
const modalContainerExCourse = document.querySelector(".wrapper-examincation");
addExCourseBtn.addEventListener("click", function (event) {
    event.preventDefault();
    modalAddExCourse.classList.add("open");
})

modalAddExCourse.addEventListener("click", function () {
    modalAddExCourse.classList.remove("open");
})

modalContainerExCourse.addEventListener("click", function (event) {
    event.stopPropagation();
})

const invoiceBtn = document.querySelectorAll("button.invoice");
const modalCreateMedicalBill = document.querySelector(".modal-create-medical-bill");
const modalContainerCreateMedicalBill = document.querySelector(".modal-create-medical-bill table")
for (let i = 0; i < invoiceBtn.length; i++) {
    invoiceBtn[i].addEventListener("click", function () {
        const patientID = document.getElementById(`patient_id_${i}`)
        const patientFullName = document.getElementById(`patient_full_name_${i}`)
        const patientLabel = document.getElementById('patient_name')
        const dayOfExamLabel = document.getElementById('day_of_exam')
        const patientIDInput = document.getElementById('patient_id_input')
        const dayOfExamInput = document.getElementById('day_of_exam_input')

        patientLabel.textContent = patientLabel.textContent + ' ' + patientFullName.textContent
        dayOfExamLabel.textContent = dayOfExamLabel.textContent + ' ' + moment().format('YYYY/MM/D')

        patientIDInput.value = patientID.textContent
        dayOfExamInput.value = moment().format('YYYY/MM/D')

        modalCreateMedicalBill.classList.add("open");
    })
}

modalCreateMedicalBill.addEventListener("click", function () {
    const patientLabel = document.getElementById('patient_name')
    const dayOfExamLabel = document.getElementById('day_of_exam')
    const patientIDInput = document.getElementById('patient_id_input')
    const dayOfExamInput = document.getElementById('day_of_exam_input')

    patientLabel.textContent = 'Patient Name:'
    dayOfExamLabel.textContent = 'Examination:'

    patientIDInput.value = ''
    dayOfExamInput.value = ''

    modalCreateMedicalBill.classList.remove("open");
})

modalContainerCreateMedicalBill.addEventListener("click", function (e) {
    e.stopPropagation();
})

const medicines = document.getElementsByClassName('medicines')
const addMedicineRow = document.getElementById('add-medicine-row')
const isAddMedicineInput = document.getElementById('is_add_medicine')

for (let i = 0; i < medicines.length; i++) {
    medicines[i].addEventListener('click', (e) => {
        for (let j = 0; medicines_list.length; j++) {
            if (medicines_list[j].medicine_name === e.target.textContent) {
                const newRow = document.createElement('tr')
                newRow.classList.add('medicine-row')
                newRow.innerHTML = `<td>${medicines_list[j].id}</td>
                                <input type="hidden" value="${medicines_list[j].id}" name="medicine_id" id="medicine_id" />
                                <td>${medicines_list[j].medicine_name}</td>
                                <td>${medicines_list[j].medicine_unit}</td>
                                <td><input type="number" name="amount" id="amount" required /></td>
                                <td>${medicines_list[j].direction_for_use}</td>
                                <td><a onclick="removeMedicineRow(this)" class="btn-remove-medicine"><i class="fa-solid fa-x"></i></a></td>`
                addMedicineRow.parentNode.insertBefore(newRow, addMedicineRow.nextSibling);
                isAddMedicineInput.value = 'true'
                modalAddMedicine.classList.remove("open");
                break
            }
        }
    })
}

const packages = document.getElementsByClassName('packages')

for (let i = 0; i < packages.length; i++) {
    packages[i].addEventListener('click', (e) => {
        for (let j = 0; j < packages_list.length; j++) {
            if (packages_list[j].packages_name === e.target.textContent) {
                const input = document.getElementById('packages_id')
                input.value = packages_list[j].id
                addExCourseBtn.innerHTML = packages_list[j].packages_name
                addExCourseBtn.style.color = 'green'
                modalAddExCourse.classList.remove("open");
                break
            }
        }
    })
}

function removeMedicineRow(removeBtn){
    const medicineRow = removeBtn.closest('.medicine-row');
    medicineRow.remove()
    const medicineRows = document.getElementsByClassName('medicine-row')
    if (medicineRows.length <= 0) isAddMedicineInput.value = null
}