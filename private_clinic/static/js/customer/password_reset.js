const btnPasswordReset = document.querySelector('.btn-password-reset')

btnPasswordReset.addEventListener('click', (e) => {
    e.preventDefault();
    showPreLoading();

    const changePasswordForm = document.getElementById('change-password-form')
    const newPassword = document.getElementById('new_password')
    const confirmNewPassword = document.getElementById('confirm_new_password')

    if (newPassword.value.trim() === confirmNewPassword.value.trim()) changePasswordForm.submit()
    else {
        setTimeout(hidePreLoading, 1000)
        setTimeout(() => {
            toast({
                title: 'Password reset failed',
                message: 'Passwords must match.',
                type: 'error',
            })
        }, 1100)
    }
})