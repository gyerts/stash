from Library.User import User


class Person(User):
    def __init__(self, dict_reviewer):
        super().__init__(dict_reviewer["user"])
        self.role = dict_reviewer["role"]
        self.approved = dict_reviewer["approved"]
