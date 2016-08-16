from Library.Path import Path
from Library.Link import Link
from Library.Comment import Comment

class File:
    def __init__(self, owner, stash, url, dict_file):
        self.owner = owner

        self.stash = stash
        self.parent_url = url

        self.contentId = dict_file["contentId"]
        self.path = Path(self, dict_file["path"])
        self.percentUnchanged = dict_file["percentUnchanged"]
        self.type = dict_file["type"]
        self.nodeType = dict_file["nodeType"]
        self.link = Link(self, dict_file["link"])
        self.links = dict_file["links"]

        try:
            self.executable = dict_file["executable"]
        except:
            self.executable = None

        self.__comments = None

        print(url, "->", self.owner, "->", self.path.toString)

    def get_owner(self):
        return self.owner.get_owner() + " -> File: contentId=" + self.contentId

    def show(self, tab="    "):
        print(tab, "contentId: ",        self.contentId)
        print(tab, "path: ",             self.path)
        print(tab, "percentUnchanged: ", self.percentUnchanged)
        print(tab, "type: ",             self.type)
        print(tab, "nodeType: ",         self.nodeType)
        print(tab, "link: ",             self.link)
        print(tab, "links: ",            self.links)
        print(tab, "executable: ",       self.executable)

    def get_comments(self):
        if self.__comments is None:
            url = self.parent_url + "/comments?path=%s" % self.path.toString
            print("URL ------------->", url)
            values = self.stash.rest_request(url)["values"]
            for comment in values:
                self.__comments.append(Comment(self, comment))
        else:
            return list()
