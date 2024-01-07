from private_clinic import views, fetcher
from private_clinic.app import app

app.add_url_rule('/', 'index', views.index)
app.add_url_rule('/about', 'about', views.about)
app.add_url_rule('/medicine', 'medicine', views.medicine)
app.add_url_rule('/notification', 'notification', views.notification)
app.add_url_rule('/doctor', 'doctor', views.doctor)
app.add_url_rule('/authentication', 'authentication', views.authentication)
app.add_url_rule('/healthcare-staff', 'healthcare_staff', views.healthcare_staff)

app.add_url_rule('/authentication/signout', 'signout', views.signout)
app.add_url_rule('/authentication/signup', 'signup', views.signup, methods=['GET', 'POST'])
app.add_url_rule('/authentication/signin', 'signin', views.signin, methods=['GET', 'POST'])
app.add_url_rule('/authentication/forgot-password', 'forgot_password', views.forgot_password, methods=['GET', 'POST'])
app.add_url_rule('/authentication/reset-with-token/<token>', 'reset_with_token', views.reset_with_token, methods=['POST'])

app.add_url_rule('/user/appointment', 'appointment', views.appointment, methods=['GET', 'POST'])
app.add_url_rule('/user/profile-settings/<slug>', 'profile_settings', views.profile_settings, methods=['GET', 'POST'])

app.add_url_rule('/employee/login', 'employee_login', views.empoyee_login)
app.add_url_rule('/employee/nurse', 'employee_nurse', views.employee_nurse)

app.add_url_rule('/mail/confirm/<token>', 'confirm_email', views.confirm_email)
app.add_url_rule('/mail/resend', 'resend_confirmation', views.resend_confirmation)
app.add_url_rule('/mail/password-reset/<token>', 'password_reset', views.password_reset)

app.add_url_rule('/api/authentication/check-signin-infor', 'check_signin_infor', fetcher.check_signin_infor, methods=['POST'])
app.add_url_rule('/api/authentication/check-signup-infor', 'check_signup_infor', fetcher.check_signup_infor, methods=['POST'])
app.add_url_rule('/api/authentication/check-profile-infor', 'check_profile_infor', fetcher.check_profile_infor, methods=['POST'])
app.add_url_rule('/api/authentication/check-account-exists', 'check_account_exists', fetcher.check_account_exists, methods=['POST'])
app.add_url_rule('/api/appointment/check-appointment-availability', 'check_appointment_availability',
                 fetcher.check_appointment_availability, methods=['POST'])
