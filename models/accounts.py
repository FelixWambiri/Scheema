class Accounts:
    def __init__(self):
        self.users = {}

    def add_new_user(self, user):
        if user.id in self.users:
            raise KeyError("User already exists")
        else:
            self.users.update({user.id: user})

    def delete_user(self, user):
        if user.id not in self.users:
            raise KeyError("user doesnt exist")
        else:
            self.users.pop(user)

    def get_specific_user(self, username):
        if username in self.users:
            return self.users[username]
