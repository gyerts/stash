from Library.Link import Link
from Library.Ref import Ref
from Library.Person import Person


class PullRequest:
    def __init__(self, stash, dict_pull_request):
        self.id           = dict_pull_request["id"]
        self.version      = dict_pull_request["version"]
        self.title        = dict_pull_request["title"]
        self.description  = dict_pull_request["description"]
        self.state        = dict_pull_request["state"]
        self.open         = dict_pull_request["open"]
        self.closed       = dict_pull_request["closed"]
        self.createdDate  = dict_pull_request["createdDate"]
        self.updatedDate  = dict_pull_request["updatedDate"]
        self.fromRef      = Ref(stash, dict_pull_request["fromRef"])
        self.toRef        = Ref(stash, dict_pull_request["toRef"])

        self.author       = Person(dict_pull_request["author"])
        self.reviewers    = self.__get_reviewers(dict_pull_request["reviewers"])

        self.participants = dict_pull_request["participants"]
        self.attributes   = dict_pull_request["attributes"]
        self.link         = Link(dict_pull_request["link"])
        self.links        = dict_pull_request["links"]


    def __get_reviewers(self, dict_users):
        reviewers = list()
        for user in dict_users:
            reviewers.append(Person(user))
        return reviewers

    def show(self):
        print("   --->   PullRequest.title", self.title)
