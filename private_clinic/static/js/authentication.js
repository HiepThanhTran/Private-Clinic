const forgotPasswordForm = document.querySelector('.forgot-password-form')
const signInForm = document.querySelector('.sign-in-form')
const signUpForm = document.querySelector('.sign-up-form')

signInForm.addEventListener('submit', (e) => {
    e.preventDefault()
    showPreLoading()

    const usernameSignIn = document.getElementById('username_signin');
    const passwordSignIn = document.getElementById('password_signin');

    fetch('/api/authentication/check-signin-infor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username_signin: usernameSignIn.value.toString(),
            password_signin: passwordSignIn.value.toString(),
        })
    }).then(response => response.json())
        .then(data => {
            if (data.status_code === 200) signInForm.submit()
            else {
                setTimeout(() => {
                    toast({
                        title: 'Sign in failed',
                        message: data.message,
                        type: 'error',
                    })
                }, 1100)
            }
        })
        .catch(error => {
            console.log(error)
        })
        .finally(() => {
            hidePreLoading()
        })
})

signUpForm.addEventListener('submit', (e) => {
    e.preventDefault()
    showPreLoading()

    const usernameSignUp = document.getElementById('username_signup');
    const emailSignUp = document.getElementById('email_signup');
    const passwordSignUp = document.getElementById('password_signup');
    const confirmPasswordSignUp = document.getElementById('confirm_password_signup');

    if (passwordSignUp.value.trim() !== confirmPasswordSignUp.value.trim()) {
        toast({
            title: 'Sign up failed',
            message: 'Passwords must match.',
            type: 'error',
        });
    } else {
        fetch('/api/authentication/check-signup-infor', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username_signup: usernameSignUp.value.toString(),
                email_signup: emailSignUp.value.toString(),
            })
        }).then(response => response.json()
            .then(data => {
                if (data.status_code === 200) signUpForm.submit()
                else {
                    setTimeout(() => {
                        toast({
                            title: 'Sign up failed',
                            message: data.message,
                            type: 'error',
                        })
                    }, 1100)
                }
            })
            .catch(error => {
                console.log(error)
            })
            .finally(() => {
                hidePreLoading()
            }))
    }
})

forgotPasswordForm.addEventListener('submit', (e) => {
    e.preventDefault()
    showPreLoading()

    const email = document.getElementById('email')

    fetch('/api/authentication/check-account-exists', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email.value.toString(),
        })
    }).then(response => response.json()
        .then(data => {
            if (data.status_code === 200) forgotPasswordForm.submit()
            else {
                setTimeout(() => {
                    toast({
                        title: 'Request failed',
                        message: data.message,
                        type: 'error',
                    })
                }, 1100)
            }
        })
        .catch(error => {
            console.log(error)
        })
        .finally(() => {
            hidePreLoading()
        })
    )
})