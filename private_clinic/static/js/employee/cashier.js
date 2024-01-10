let prescriptions = {}
window.onload = (e) => {
    fetch('/api/employee/doctor/load-medicine-by-medical-bill-id', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    }).then(response => response.json())
        .then(data => {
            prescriptions = data
        })
        .catch(error => {
            console.log(error)
        })
}

/* Moal Detail */
const detailBtn = document.querySelectorAll(".detail");
const modalDetail = document.querySelector(".modal-detail");
const modalDetailContainer = document.querySelector(".modal-detail table");

for (let i = 0; i < detailBtn.length; i++) {
    detailBtn[i].addEventListener("click", function () {
        const medicalBillID = document.getElementById(`medical_bill_id_${i}`)
        const medicalBillExaminationDate = document.getElementById(`medical_bill_examination_date_${i}`)
        const medicalBillFullName = document.getElementById(`medical_bill_full_name_${i}`)
        const medicalBillSymptoms = document.getElementById(`medical_bill_symptoms_${i}`)
        const medicalBillDiagnostic = document.getElementById(`medical_bill_diagnostic_${i}`)

        const patientNameLabel = document.getElementById('patient_name')
        const dayOfExamLabel = document.getElementById('day_of_exam')
        const symptomLabel = document.getElementById('symptoms')
        const diagnosticLabel = document.getElementById('diagnostic')

        patientNameLabel.textContent = patientNameLabel.textContent + ' ' + medicalBillFullName.value.toString()
        dayOfExamLabel.textContent = dayOfExamLabel.textContent + ' ' + medicalBillExaminationDate.textContent
        symptomLabel.textContent = symptomLabel.textContent + ' ' + medicalBillSymptoms.value.toString()
        diagnosticLabel.textContent = diagnosticLabel.textContent + ' ' + medicalBillDiagnostic.value.toString()

        const medicalBillDetails = document.getElementById('medical-bill-details')
        for (let i = 0; i < prescriptions.length; i++) {
            if (parseInt(prescriptions[i].medical_bill_id) === parseInt(medicalBillID.textContent)) {
                const medicineRow = document.createElement('tr')
                medicineRow.classList.add('medicine-row')
                medicineRow.innerHTML = `<th>${prescriptions[i].id}</th>
                                        <th>${prescriptions[i].medicine_name}</th>
                                        <th>${prescriptions[i].medicine_unit}</th>
                                        <th>${prescriptions[i].amount}</th>
                                        <th>${prescriptions[i].direction_for_use}</th>`
                medicalBillDetails.appendChild(medicineRow)
            }
        }

        modalDetail.classList.add("open");
    })
}

modalDetail.addEventListener("click", function () {
    const patientNameLabel = document.getElementById('patient_name')
    const dayOfExamLabel = document.getElementById('day_of_exam')
    const symptomLabel = document.getElementById('symptoms')
    const diagnosticLabel = document.getElementById('diagnostic')

    patientNameLabel.textContent = 'Patient Name:'
    dayOfExamLabel.textContent = 'Examination day:'
    symptomLabel.textContent = 'Symptoms:'
    diagnosticLabel.textContent = 'Diagnostic:'

    const medicineRows = document.getElementsByClassName('medicine-row')
    while (medicineRows.length > 0) medicineRows[0].remove()

    modalDetail.classList.remove("open");
})

modalDetailContainer.addEventListener("click", function (event) {
    event.stopPropagation();
})

/* Modal Print */
const invoiceBtn = document.querySelectorAll(".invoice");
const modalPrint = document.querySelector(".modal-print");
const modalPrintContainer = document.querySelector(".modal-print table");
for (let i = 0; i < invoiceBtn.length; i++) {
    invoiceBtn[i].addEventListener("click", function () {
        const medicalBillID = document.getElementById(`medical_bill_id_${i}`)
        const medicalBillExaminationDate = document.getElementById(`medical_bill_examination_date_${i}`)
        const medicalBillFullName = document.getElementById(`medical_bill_full_name_${i}`)
        const patientID = document.getElementById(`medical_bill_patient_${i}`)

        const billNameLabel = document.getElementById('bill_name')
        const billDayOfExam = document.getElementById('bill_day_of_exam')
        const billFee = document.getElementById('bill_fee')
        const billMedicineFee = document.getElementById('bill_medicine_fee')
        const billTotalPrice = document.getElementById('bill_total_price')

        const patientIDInput = document.getElementById('patient_id')
        const medicalBillIDInput = document.getElementById('medical_bill_id')
        const examinationDateInput = document.getElementById('examination_date')
        const preExaminationInput = document.getElementById('pre_examination')
        const medicineMoneyInput = document.getElementById('medicine_money')
        const totalPriceInput = document.getElementById('total_price')

        billNameLabel.textContent = billNameLabel.textContent + ' ' + medicalBillFullName.value.toString()
        billDayOfExam.textContent = billDayOfExam.textContent + ' ' + medicalBillExaminationDate.textContent

        let fee = 0
        let medicineFee = 0
        let totalPrice = 0

        for (let i = 0; i < prescriptions.length; i++) {
            if (parseInt(prescriptions[i].medical_bill_id) === parseInt(medicalBillID.textContent)) {
                fee = prescriptions[i].package_price
                medicineFee += prescriptions[i].medicine_price
            }
        }
        totalPrice = fee + medicineFee

        billFee.textContent = billFee.textContent + ' ' + fee
        billMedicineFee.textContent = billMedicineFee.textContent + ' ' + medicineFee
        billTotalPrice.textContent = billTotalPrice.textContent + ' ' + totalPrice

        patientIDInput.value = patientID.value
        medicalBillIDInput.value = medicalBillID.textContent
        preExaminationInput.value = fee
        medicineMoneyInput.value = medicineFee
        totalPriceInput.value = totalPrice
        examinationDateInput.value = medicalBillExaminationDate.textContent

        modalPrint.classList.add("open");
    })
}
modalPrint.addEventListener("click", function () {
    const billNameLabel = document.getElementById('bill_name')
    const billDayOfExam = document.getElementById('bill_day_of_exam')
    const billFee = document.getElementById('bill_fee')
    const billMedicineFee = document.getElementById('bill_medicine_fee')
    const billTotalPrice = document.getElementById('bill_total_price')

    billNameLabel.textContent = 'Name:'
    billDayOfExam.textContent = 'Day of the examination:'
    billFee.textContent = 'Examination fee:'
    billMedicineFee.textContent = 'Medicine money:'
    billTotalPrice.textContent = 'Total:'

    const patientIDInput = document.getElementById('patient_id')
    const examination_date = document.getElementById('examination_date')
    const pre_examination = document.getElementById('pre_examination')
    const medicine_money = document.getElementById('medicine_money')
    const total_price = document.getElementById('total_price')
    const medical_bill_id = document.getElementById('medical_bill_id')

    patientIDInput.value = null
    examination_date.value = null
    pre_examination.value = null
    medicine_money.value = null
    total_price.value = null
    medical_bill_id.value = null

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