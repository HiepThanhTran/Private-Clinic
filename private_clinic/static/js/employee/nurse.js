const manageBtn = document.querySelector("#appointment-list-btn");
const examinationBtn = document.querySelector("#create-examination-btn");
const tableManage = document.querySelector(".table-manage");
const tableManageTitle = document.querySelector(".manage-title");
const tableEx = document.querySelector(".table-examination");
const tableExTitle = document.querySelector(".examination-title");
const exBtn = document.querySelector(".ex-btn");
const appointmentBtn = document.querySelector("#appointment-btn");
const appointmentForm = document.querySelector(".appointment-form");
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
    appointmentForm.style.display = "none";
    appointmentBtn.classList.remove("active");
})

examinationBtn.addEventListener("click", function (event) {
    examinationBtn.classList.add("active");
    tableExTitle.style.display = "block";
    tableEx.style.display = "flex";
    tableEx.style.justifyContent = "center";
    tableEx.style.alignItems = "center";
    exBtn.style.display = "flex";
    exBtn.style.jutifyContent = "center";
    exBtn.style.alignItems = "center";
    tableManageTitle.style.display = "none";
    tableManage.style.display = "none";
    manageBtn.classList.remove("active");
})

appointmentBtn.addEventListener("click", function () {
    appointmentBtn.classList.add("active");
    appointmentForm.style.display = "block";
    tableManageTitle.style.display = "none";
    tableManage.style.display = "none";
    manageBtn.classList.remove("active");
    tableExTitle.style.display = "none";
    tableEx.style.display = "none";
    exBtn.style.display = "none";
    examinationBtn.classList.remove("active");
})

const tableBody = document.getElementById('create-examination-table')
const rowsToDelete = tableBody.getElementsByClassName('tr-body');
const dayOfExamInput = document.getElementById('day_of_exam')
const btnCreateExamList = document.querySelector('.btn-ex')

dayOfExamInput.addEventListener('change', () => {
    showPreLoading()

    fetch('/api/authentication/load-examination-schedule-list-by-date', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            day_of_exam: dayOfExamInput.value.toString(),
        })
    }).then(response => response.json())
        .then(data => {
            if (data.length) {
                while (rowsToDelete.length > 0) rowsToDelete[0].remove()
                btnCreateExamList.disabled = false
                data.forEach(schedule => {
                    const tr = document.createElement('tr')
                    tr.classList.add('tr-body')
                    const dateObject = new Date(schedule.dob);
                    const dob = dateObject.toISOString().split('T')[0];
                    tr.innerHTML = `<td>${schedule.id}<input type="hidden" name="examination_id" value="${schedule.id}"/></td>
                                    <td>${schedule.full_name}</td>
                                    <td>${schedule.gender}</td>
                                    <td>${dob}</td>
                                    <td>${schedule.address}</td>`
                    tableBody.appendChild(tr)
                })
            } else {
                while (rowsToDelete.length > 0) rowsToDelete[0].remove()
                btnCreateExamList.disabled = true
                const tr = document.createElement('tr')
                tr.classList.add('tr-body')
                tr.innerHTML = `<td>...</td>
                                <td>...</td>
                                <td>...</td>
                                <td>...</td>
                                <td>...</td>`
                tableBody.appendChild(tr)
            }
        })
        .catch(error => {
            console.log(error)
        })
        .finally(() => {
            hidePreLoading()
        })
})