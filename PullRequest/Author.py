from Library.User import User

class Author():
    def __init__(self, owner, dict_author):
        self.owner = owner

        self.user     = User(self, dict_author["user"])
        self.role     = dict_author["role"]
        self.approved = dict_author["approved"]

    def get_owner(self):
        return self.owner.get_owner() + " -> Comment: id=" + self.user.name