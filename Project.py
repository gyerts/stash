from Repository import Repository
from Link import Link


class Project:
    def __init__(self, stash, dict_project):
        self.stash = stash

        self.name   = dict_project["name"]
        self.type   = dict_project["type"]
        self.id     = dict_project["id"]
        self.key    = dict_project["key"]
        self.links  = dict_project["links"]
        self.public = dict_project["public"]
        self.link   = Link(dict_project["link"])

    def get_all_repositories(self):
        repositories = list()
        for repository in self.stash.rest_request(self.stash.path_to_stash + self.link.url + "/repos")["values"]:
            repositories.append(Repository(self.stash, self, repository))

        return repositories

    def show(self):
        print("name   =", self.name)
        print("type   =", self.type)
        print("id     =", self.id)
        print("key    =", self.key)
        print("links  =", self.links)
        print("public =", self.public)
        self.link.show()
        print("\n\n")
