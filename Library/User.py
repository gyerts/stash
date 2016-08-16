from Library.Link import Link

class User:
    def __init__(self, owner, dict_user):
        self.owner = owner

        self.name = dict_user["name"]
        self.emailAddress = dict_user["emailAddress"]

        try:
            self.id          = dict_user["id"]
            self.displayName = dict_user["displayName"]
            self.active      = dict_user["active"]
            self.slug        = dict_user["slug"]
            self.type        = dict_user["type"]
            self.link        = Link(self, dict_user["link"])
            self.links       = dict_user["links"]

        except:
            self.id = self.displayName = self.active = self.slug = \
                self.type = self.link = self.links = None

    def show(self, tab="   "):
        print(tab + "author:")
        print(tab + tab + "name =", self.name)
        print(tab + tab + "emailAddress =", self.emailAddress)

        try:
            print(tab + tab + "id:", self.id)
            print(tab + tab + "displayName:", self.displayName)
            print(tab + tab + "active:", self.active)
            print(tab + tab + "slug:", self.slug)
            print(tab + tab + "type:", self.type)
            self.link.show(tab + "      ")
            print(tab + tab + "links:", self.links)

        except Exception as ex:
            print(tab + "User.Exception [OK BEHAVIOUR]: ", ex)

    def get_owner(self):
        return self.owner.get_owner() + " -> User: name=" + self.name
