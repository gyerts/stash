from Library.User import User

class Author():
    def __init__(self, dict_author):
        self.user     = User(dict_author["user"])
        self.role     = dict_author["role"]
        self.approved = dict_author["approved"]
