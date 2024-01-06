const btnApopointmentForm = document.querySelector('.form-appointment__btn')
const appointmentForm = document.getElementById('appointment-form')
const btnClose = document.querySelector('.btn-modal-close')

btnApopointmentForm.addEventListener('click', (e) => {
    e.preventDefault()
})

appointmentForm.addEventListener('submit', (e) => {
    e.preventDefault()
    showPreLoading()

    const firstName = document.getElementById('firstname')
    const lastName = document.getElementById('lastname')
    const dob = document.getElementById('dob')
    const gender = document.getElementById('gender')
    const email = document.getElementById('email')
    const phone_number = document.getElementById('phone')
    const address = document.getElementById('address')
    const day_of_exam = document.getElementById('day_of_exam')
    const time_of_exam = document.getElementById('time_of_exam')

    fetch('/appointment', {
        method: 'POST', headers: {
            'Content-Type': 'application/json'
        }, body: JSON.stringify({
            first_name: firstName.value.toString(),
            last_name: lastName.value.toString(),
            dob: dob.value.toString(),
            gender: gender.value.toString(),
            email: email.value.toString(),
            phone_number: phone_number.value.toString(),
            address: address.value.toString(),
            day_of_exam: day_of_exam.value.toString(),
            time_of_exam: time_of_exam.value.toString(),
        })
    }).then(response => response.json())
        .then(data => {
            const type = data.status_code === 200 ? 'success' : 'error'
            setTimeout(() => {
                if (data.status_code === 401) day_of_exam.focus()
                if (data.status_code === 402) time_of_exam.focus()
            }, 1500)
            setTimeout(() => {
                toast({
                    title: 'Make an appointment',
                    message: data.message,
                    type: type,
                })
                btnClose.click()
                if (data.status_code === 200) appointmentForm.reset()
            }, 1100)
        })
        .catch(error => {
            console.log(error)
        })
        .finally(() => {
            setTimeout(hidePreLoading, 1000)
        })
})