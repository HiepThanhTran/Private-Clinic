from private_clinic import dao


def create_account(username, password):
    return dao.create_account(username=username, password=password)
