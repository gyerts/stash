from Library.Link import Link
from Library.Ref import Ref
from Library.Person import Person
from Commit import Commit


class PullRequest:
    def __init__(self, stash, url, dict_pull_request):
        self.url = url + "/pull-requests/1"
        self.stash = stash

        self.id           = dict_pull_request["id"]
        self.version      = dict_pull_request["version"]
        self.title        = dict_pull_request["title"]
        self.description  = dict_pull_request["description"]
        self.state        = dict_pull_request["state"]
        self.open         = dict_pull_request["open"]
        self.closed       = dict_pull_request["closed"]
        self.createdDate  = dict_pull_request["createdDate"]
        self.updatedDate  = dict_pull_request["updatedDate"]
        self.fromRef      = Ref(stash, "fromRef", dict_pull_request["fromRef"])
        self.toRef        = Ref(stash, "toRef", dict_pull_request["toRef"])

        self.author       = Person(dict_pull_request["author"])
        self.reviewers    = self.__get_reviewers(dict_pull_request["reviewers"])

        self.participants = dict_pull_request["participants"]
        self.attributes   = dict_pull_request["attributes"]
        self.link         = Link(dict_pull_request["link"])
        self.links        = dict_pull_request["links"]

        self.commits = self.__get_commits()
        self.changed_files = self.__get_files()

    def __get_files(self):
        url = self.url + "/commits"
        files = list()
        ans = self.stash.rest_request(url)
        for file in ans['values']:
            files.append(Commit(file))
        return files


    def __get_commits(self):
        url = self.url + "/commits"
        commits = list()
        ans = self.stash.rest_request(url)
        for commit in ans['values']:
            commits.append(Commit(commit))
        return commits

    def __get_reviewers(self, dict_users):
        reviewers = list()
        for user in dict_users:
            reviewers.append(Person(user))
        return reviewers

    def show(self, tab="   "):
        print(tab + "id: ", self.id)
        print(tab + "version: ", self.version)
        print(tab + "title: ", self.title)
        print(tab + "description: ", self.description)
        print(tab + "state: ", self.state)
        print(tab + "open: ", self.open)
        print(tab + "closed: ", self.closed)
        print(tab + "createdDate: ", self.createdDate)
        print(tab + "updatedDate: ", self.updatedDate)
        self.fromRef.show(tab)
        self.toRef.show(tab)

        self.author.show(tab)

        print(tab + "reviewers: ")
        for reviewer in self.reviewers:
            reviewer.show(tab + tab)

        print(tab + "participants: ", self.participants)
        print(tab + "attributes: ", self.attributes)
        self.link.show(tab)
        print(tab + "links: ", self.links)

        print(tab + "commits: ")
        for commit in self.commits:
            commit.show(tab + "   ")
