from Repository import Repository
from Library.Link import Link


class Project:
    def __init__(self, owner, stash, dict_project):
        self.owner = owner
        self.stash = stash

        self.name   = dict_project["name"]
        self.type   = dict_project["type"]
        self.id     = dict_project["id"]
        self.key    = dict_project["key"]
        self.links  = dict_project["links"]
        self.public = dict_project["public"]
        self.link   = Link(self, dict_project["link"])

        self.url = self.stash.url + self.link.url

    def get_owner(self):
        return self.owner.get_owner() + " -> Project: name=" + self.name

    def get_all_repositories(self):
        repositories = list()
        for repository in self.stash.rest_request(self.url + "/repos")["values"]:
            repositories.append(
                Repository(
                    owner=self,
                    stash=self.stash,
                    project=self,
                    dict_repository=repository
                )
            )

        return repositories

    def get_repository_by_name(self, name):
        # to get changed files -------------------------------------
        example = "{server}/rest/api/1.0/projects/{project_id}/repos"
        # ----------------------------------------------------------
        for repository in self.stash.rest_request(example, self.url + "/repos")["values"]:
            repo = Repository(
                owner=self,
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
