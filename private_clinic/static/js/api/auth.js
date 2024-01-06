const btnSignInAndSignUp = document.querySelectorAll('.btn-signin-and-signup');

for (const btn of btnSignInAndSignUp) {
    btn.addEventListener('click', async (e) => {
        e.preventDefault();
        showPreLoading();

        const type = btn.getAttribute('my-type').toString();
        const handleSignIn = async () => {
            const signInForm = document.querySelector('.sign-in-form')
            const usernameSignIn = document.getElementById('username_signin');
            const passwordSignIn = document.getElementById('password_signin');

            try {
                const response = await fetch('/api/authentication/check-signin-infor', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username_signin: usernameSignIn.value.toString(),
                        password_signin: passwordSignIn.value.toString(),
                    })
                });
                const data = await response.json();

                if (data.status_code === 200) {
                    signInForm.submit()
                } else {
                    setTimeout(() => {
                        toast({
                            title: 'Sign in failed',
                            message: data.message,
                            type: 'error',
                        })
                    }, 1100)
                }
            } catch (error) {
                console.log(error);
            } finally {
                setTimeout(hidePreLoading, 1000)
            }
        };

        const handleSignUp = async () => {
            const signUpForm = document.querySelector('.sign-up-form')
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
                try {
                    const response = await fetch('/api/authentication/check-signup-infor', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            username_signup: usernameSignUp.value.toString(),
                            email_signup: emailSignUp.value.toString(),
                        })
                    });
                    const data = await response.json();

                    if (data.status_code === 200) {
                        signUpForm.submit()
                    } else {
                        setTimeout(() => {
                            toast({
                                title: 'Sign in failed',
                                message: data.message,
                                type: 'error',
                            })
                        }, 1100)
                    }
                } catch (error) {
                    console.log(error);
                } finally {
                    setTimeout(hidePreLoading, 1000)
                }
            }
        };

        if (type === 'signin') {
            await handleSignIn();
        } else if (type === 'signup') {
            await handleSignUp();
        }
    });
}

const btnForgotPassword = document.querySelector('.btn-forgot-password')

btnForgotPassword.addEventListener('click', (e) => {
    e.preventDefault();
    showPreLoading();

    const forgotPasswordForm = document.querySelector('.forgot-password-form')
    const forgotPasswordInfor = document.getElementById('infor_forgotpassword')

    fetch('/api/authentication/check-account-exists', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            infor: forgotPasswordInfor.value.toString(),
        })
    }).then(response => response.json())
        .then(data => {
            if (data.status_code === 200) {
                forgotPasswordForm.submit()
            } else {
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
            setTimeout(hidePreLoading, 1000)
        })
})