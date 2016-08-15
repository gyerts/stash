class Path:
    def __init__(self, dict_path):
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
