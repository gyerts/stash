from Library.User import User


class Person(User):
    def __init__(self, dict_reviewer):
        super().__init__(dict_reviewer["user"])
        self.role = dict_reviewer["role"]
        self.approved = dict_reviewer["approved"]

    def show(self, tab="   "):
        print(tab + "/* ----------- User -----------")
        super().show(tab)
        print(tab + "role:", self.role)
        print(tab + "approved:", self.approved)
        print(tab + "----------- User ----------- */")

