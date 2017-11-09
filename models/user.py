from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, email, password, confirm_password):
        self.id = username
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
 