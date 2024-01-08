const btnApopointmentForm = document.querySelector('.form-appointment__btn')
const appointmentForm = document.getElementById('appointment-form')
const btnClose = document.querySelector('.btn-modal-close')

btnApopointmentForm.addEventListener('click', (e) => {
    e.preventDefault()
})

appointmentForm.addEventListener('submit', (e) => {
    e.preventDefault()
    showPreLoading()

    const day_of_exam = document.getElementById('day_of_exam')
    const time_of_exam = document.getElementById('time_of_exam')

    fetch('/api/appointment/check-appointment-availability', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            day_of_exam: day_of_exam.value.toString(),
            time_of_exam: time_of_exam.value.toString(),
        })
    }).then(response => response.json())
        .then(data => {
            if (data.status_code === 200) appointmentForm.submit()
            else {
                setTimeout(() => {
                    toast({
                        title: 'Registered failed',
                        message: data.message,
                        type: 'error',
                    })
                    btnClose.click()
                }, 1100)
                setTimeout(() => {
                    if (data.status_code === 401) day_of_exam.focus()
                    if (data.status_code === 402) time_of_exam.focus()
                }, 1500)
            }
        })
        .catch(error => {
            console.log(error)
        })
        .finally(() => {
            hidePreLoading()
        })
})