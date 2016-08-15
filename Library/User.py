from Library.Link import Link

class User:
    def __init__(self, dict_user):
        self.name = dict_user["name"]
        self.emailAddress = dict_user["emailAddress"]

        try:
            self.id          = dict_user["id"]
            self.displayName = dict_user["displayName"]
            self.active      = dict_user["active"]
            self.slug        = dict_user["slug"]
            self.type        = dict_user["type"]
            self.link        = Link(dict_user["link"])
            self.links       = dict_user["links"]

        except Exception as ex:
            print("User.Exception [OK BEHAVIOUR]: ", ex)

    def show(self):
        print("author:")
        print("    name         =", self.name)
        print("    emailAddress =", self.emailAddress)
