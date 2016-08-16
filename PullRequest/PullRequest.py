from Library.Link import Link
from Library.Ref import Ref
from Library.Person import Person
from Commit import Commit
from Library.File import File
from Library.Comment import Comment


class PullRequest:
    def __init__(self, owner, stash, url, dict_pull_request):
        self.owner = owner

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
        self.fromRef      = Ref(self, stash, "fromRef", dict_pull_request["fromRef"])
        self.toRef        = Ref(self, stash, "toRef", dict_pull_request["toRef"])

        self.url = url + "/pull-requests/" + str(self.id)

        self.author       = Person(self, dict_pull_request["author"])
        self.reviewers    = self.__get_reviewers(dict_pull_request["reviewers"])

        self.participants = dict_pull_request["participants"]
        self.link         = Link(self, dict_pull_request["link"])
        self.links        = dict_pull_request["links"]

        try:
            self.attributes = dict_pull_request["attributes"]
        except:
            self.attributes = None

        self.commits = self.__get_commits()
        self.changed_files = self.__get_files()
        self.comments = self.__get_comments()

    def get_owner(self):
        return self.owner.get_owner() + " -> PullRequest: id=" + str(self.id)

    def get_commit_by_id(self, id):
        for commit in self.commits:
            if commit.id == id:
                return commit
        return None

    def conteins(self, obj_commit):
        for commit in self.commits:
            if commit.id == obj_commit.id:
                return True
        return False

    def __get_comments(self):
        url = self.url + "/activities"
        # --------------------------------------------------------------------------------------------------
        example = "{server}/rest/api/1.0/projects/{project_id}/repos/{repo_slug}/pull-requests/{id_of_pull_request}/activities"
        # --------------------------------------------------------------------------------------------------
        response = self.stash.rest_request(example, url)["values"]

        comments = list()
        for activity in response:
            if "COMMENTED" == activity["action"] and "commentAnchor" not in activity:
                comments.append(Comment(self, activity))
        return comments

    def __get_comments_of_file(self, file_to_find):
        for commit in self.commits:
            for file in commit.files:
                if file.path.toString == file_to_find:
                    return file.get_comments()
        return list()

    def __get_files(self):
        files = list()
        for commit in self.commits:
            for file in commit.files:
                files.append(file.path.toString)

        return files

    def __get_commits(self):
        commits = list()
        url = self.url + "/commits"
        # --------------------------------------------------------------------------------------------------
        example = "{server}/rest/api/1.0/projects/{project_id}/repos/{repo_slug}/pull-requests/{id_of_pull_request}/commits"
        # --------------------------------------------------------------------------------------------------

        print("*****************************", url)
        ans = self.stash.rest_request(example, url)
        for commit in ans['values']:
            commits.append(Commit(self, self.parent_url, self.stash, commit, self.url))
        return commits

    def __get_changed_files(self):
        response = self.stash.rest_request(self.url + "/changes")["values"]
        files = list()
        for file in response:
            files.append(File(self.stash, self.url, file, "PullRequest/" + self.id))
        return files

    def __get_reviewers(self, dict_users):
        reviewers = list()
        for user in dict_users:
            reviewers.append(Person(self, user))
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

        print(tab + "comments: ")
        for comment in self.comments:
            print(tab + "   " + str(comment))

