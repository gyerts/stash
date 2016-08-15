from Library.Link import Link
from Library.Ref import Ref
from Library.Person import Person
from Commit import Commit
from Library.File import File


class PullRequest:
    def __init__(self, stash, url, dict_pull_request):
        self.parent_url = url
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

        self.url = url + "/pull-requests/" + str(self.id)

        self.author       = Person(dict_pull_request["author"])
        self.reviewers    = self.__get_reviewers(dict_pull_request["reviewers"])

        self.participants = dict_pull_request["participants"]
        self.link         = Link(dict_pull_request["link"])
        self.links        = dict_pull_request["links"]

        try:
            self.attributes = dict_pull_request["attributes"]
        except:
            self.attributes = None

        self.commits = self.__get_commits()
        self.changed_files = self.__get_files()

    def conteins(self, obj_commit):
        for commit in self.commits:
            if commit.id == obj_commit.id:
                return True
        return False

    def comments(self):
        return self.stash.rest_request(self.url + "/comments", "POST")

    def __get_files(self):
        files = list()
        for commit in self.commits:
            for file in commit.files:
                file.show()
                files.append(file.path.toString)

        return files

    def __get_commits(self):
        url = self.url + "/commits"
        commits = list()
        print("*****************************", url)

        ans = self.stash.rest_request(url)
        for commit in ans['values']:
            commits.append(Commit(self.parent_url, self.stash, commit))
        return commits

    def __get_changed_files(self):
        response = self.stash.rest_request(self.url + "/changes")["values"]
        files = list()
        for file in response:
            files.append(File(file))
        return files

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
        # print(tab + "attributes: ", self.attributes)
        self.link.show(tab)
        print(tab + "links: ", self.links)

        print(tab + "commits: ")
        for commit in self.commits:
            commit.show(tab + "   ")

        print(tab + "files: ")
        for file in self.changed_files:
            print(tab + "   " + file)
