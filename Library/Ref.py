from Repository import Repository
from Project import Project


class Ref:
    def __init__(self, owner, stash, name, dict_ref):
        self.owner = owner

        self.name = name
        self.id = dict_ref["id"]
        self.displayId = dict_ref["displayId"]
        self.latestChangeset = dict_ref["latestChangeset"]
        self.repository = self.create_repository(stash, dict_ref["repository"])

    def create_repository(self, stash, dict_ref):
        project = Project(self, stash, dict_ref["project"])
        return Repository(self, stash, project, dict_ref)

    def show(self, tab="   "):
        print(tab + self.name + ": ")
        print(tab + "   id:", self.id)
        print(tab + "   displayedName:", self.displayId)
        print(tab + "   latestChangeset:", self.latestChangeset)
        print(tab + "   repository.name:", self.repository.name)

    def get_owner(self):
        return self.owner.get_owner() + " -> Ref: id=" + self.id
