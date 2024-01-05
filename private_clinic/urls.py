from private_clinic import views
from private_clinic.app import app

app.add_url_rule('/', 'index', views.index)
app.add_url_rule('/about', 'about', views.about)
app.add_url_rule('/healthcare-staff', 'healthcare_staff', views.healthcare_staff)
app.add_url_rule('/auth', 'auth', views.auth)
app.add_url_rule('/appointment', 'appointment', views.appointment)
app.add_url_rule('/profile_settings', 'profile_settings', views.profile_settings)
app.add_url_rule('/recovery_password', 'recovery_password', views.recovery_password)

app.add_url_rule('/auth/signup', 'signup', views.signup, methods=['POST'])
