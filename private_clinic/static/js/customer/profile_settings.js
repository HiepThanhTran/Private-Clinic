const profileSettingsForm = document.getElementById('profile-settings-form')
const btnProfileSettingsForm = document.querySelector('.form-settings__btn')
const btnClose = document.querySelector('.btn-modal-close')

btnProfileSettingsForm.addEventListener('click', (e) => {
    e.preventDefault()
    const notiAlert = document.querySelector('.noti-alert')
    if (notiAlert) notiAlert.remove()
})

profileSettingsForm.addEventListener('submit', (e) => {
    e.preventDefault()
    showPreLoading()

    const email = document.getElementById('email')
    const phoneNumber = document.getElementById('phone_number')
    const insuranceId = document.getElementById('insurance_id')

    fetch('/api/authentication/check-profile-infor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email.value.toString(),
            phone_number: phoneNumber.value.toString(),
            insurance_id: insuranceId.value.toString()
        })
    }).then(response => response.json())
        .then(data => {
            if (data.status_code === 200) profileSettingsForm.submit()
            else {
                setTimeout(() => {
                    toast({
                        title: 'Save failed',
                        message: data.message,
                        type: 'error',
                    })
                    btnClose.click()
                }, 1100)
                setTimeout(() => {
                    if (data.status_code === 401) email.focus()
                    if (data.status_code === 402) phoneNumber.focus()
                    if (data.status_code === 403) insuranceId.focus()
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

const inputAvatarFile = document.getElementById('avatar')
const avatarImg = document.getElementById('avatar-img')

inputAvatarFile.addEventListener('change', () => {
    avatarImg.src = URL.createObjectURL(inputAvatarFile.files.item(0))
})