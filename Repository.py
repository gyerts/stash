from Library.Link import Link
from Commit import Commit


class Repository:
    def __init__(self, stash, project, dict_repository):
        self.stash = stash
        self.project = project

        self.statusMessage = dict_repository["statusMessage"]
        self.name          = dict_repository["name"]
        self.slug          = dict_repository["slug"]
        self.id            = dict_repository["id"]
        self.cloneUrl      = dict_repository["cloneUrl"]
        self.state         = dict_repository["state"]
        self.scmId         = dict_repository["scmId"]
        self.links         = dict_repository["links"]
        self.public        = dict_repository["public"]
        self.link          = Link(dict_repository["link"])

        try:
            self.forkable = dict_repository["forkable"]
        except Exception as ex:
            print("Exception: ", ex)

        self.url = "%s/repos/%s" % (project.url, self.slug)

    def commits(self, branch=None):
        url = self.url + "/commits/___branch___"

        if branch is not None:
            url = url.replace("___branch___", "?until=%s"%branch)
        else:
            url = url.replace("/___branch___", "")
        print("url: ", url)

        commits = list()
        for commit in self.stash.rest_request(url)["values"]:
            commits.append(Commit(commit))

        return commits

    def get_all_pull_requests(self, state="open"):
        """
        state could be:
            open
            merged
            declined
        """

        url = self.url + "/pull-requests?state=%s" % state
        print("url: ", url)
        return self.stash.rest_request(url)['values']

    def show(self):
        print("statusMessage =", self.statusMessage)
        print("name =", self.name)
        print("slug =", self.slug)
        print("id =", self.id)
        print("cloneUrl =", self.cloneUrl)
        print("state =", self.state)
        print("scmId =", self.scmId)
        print("links =", self.links)
        print("public =", self.public)
        print("link:")
        self.link.show()
        print('\n\n')
