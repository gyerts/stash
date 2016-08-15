from Repository import Repository
from Library.Link import Link


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

        self.url = self.stash.url + self.link.url

    def get_all_repositories(self):
        repositories = list()
        for repository in self.stash.rest_request(self.url + "/repos")["values"]:
            repositories.append(
                Repository(
                    stash=self.stash,
                    project=self,
                    dict_repository=repository
                )
            )

        return repositories

    def get_repository_by_name(self, name):
        for repository in self.stash.rest_request(self.url + "/repos")["values"]:
            repo = Repository(
                stash=self.stash,
                project=self,
                dict_repository=repository
            )
            if repo.name == name:
                return repo
        return None

    def show(self):
        print("name   =", self.name)
        print("type   =", self.type)
        print("id     =", self.id)
        print("key    =", self.key)
        print("links  =", self.links)
        print("public =", self.public)
        self.link.show()
        print("\n\n")
