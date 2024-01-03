from private_clinic import views
from private_clinic.app import app


app.add_url_rule('/', 'index', views.index)
app.add_url_rule('/auth', 'auth', views.auth)


if __name__ == '__main__':
    app.run()
