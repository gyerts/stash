from Repository import Repository
from Project import Project


class Ref:
    def __init__(self, stash, dict_ref):
        self.id = dict_ref["id"]
        self.displayId = dict_ref["displayId"]
        self.latestChangeset = dict_ref["latestChangeset"]
        self.repository = self.create_repository(stash, dict_ref["repository"])

    def create_repository(self, stash, dict_ref):
        project = Project(stash, dict_ref["project"])
        return Repository(stash, project, dict_ref)
