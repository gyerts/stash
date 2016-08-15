from Library.Path import Path
from Library.Link import Link


class File:
    def __init__(self, dict_file):
        self.contentId = dict_file["contentId"]
        self.path = Path(dict_file["path"])
        self.executable = dict_file["executable"]
        self.percentUnchanged = dict_file["percentUnchanged"]
        self.type = dict_file["type"]
        self.nodeType = dict_file["nodeType"]
        self.link = Link(dict_file["link"])
        self.links = dict_file["links"]

    def show(self, tab):
        print(tab, "contentId: ", self.contentId)
        print(tab, "path: ", self.path)
        print(tab, "executable: ", self.executable)
        print(tab, "percentUnchanged: ", self.percentUnchanged)
        print(tab, "type: ", self.type)
        print(tab, "nodeType: ", self.nodeType)
        print(tab, "link: ", self.link)
        print(tab, "links: ", self.links)
