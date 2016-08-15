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
