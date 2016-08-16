from Library.Path import Path
from Library.Link import Link
from Library.Comment import Comment

class File:
    def __init__(self, owner, stash, dict_file):
        self.owner = owner

        self.stash = stash

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

    def get_owner(self):
        return self.owner.get_owner() + " -> File: name=" + self.path.name

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
            self.__comments = list()
            # --------------------------------------------------------------------------------------------------
            example1 = "{server}/rest/api/1.0/projects/{project_id}/repos/{repo_slug}/pull-requests/{id_of_pull_request}/comments?path={path_to_file}"
            # --------------------------------------------------------------------------------------------------
            example2 = "{server}/rest/api/1.0/projects/{project_id}/repos/{repo_slug}/commits/{commit_id}/comments?path={path_to_file}"
            # --------------------------------------------------------------------------------------------------
            url = self.owner.url + "/comments?path=%s" % self.path.toString
            values = self.stash.rest_request(example1, url)["values"]

            for comment in values:
                comment = Comment(self, comment)
                self.__comments.append(comment.user.name + ": " + comment.text)

        return self.__comments
