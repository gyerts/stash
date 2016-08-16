class Path:
    def __init__(self, owner, dict_path):
        self.owner = owner

        self.components = dict_path["components"]
        self.parent = dict_path["parent"]
        self.name = dict_path["name"]
        self.extension = dict_path["extension"]
        self.toString = dict_path["toString"]

    def show(self, tab):
        print(tab, self.components, self.components)
        print(tab, self.parent, self.parent)
        print(tab, self.name, self.name)
        print(tab, self.extension, self.extension)
        print(tab, self.toString, self.toString)

    def get_owner(self):
        return self.owner.get_owner() + " -> Path: toString=" + self.toString
