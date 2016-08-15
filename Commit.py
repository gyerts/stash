
class Commit:
    def __init__(self, dict_commit):
        self.author = Commit.Author(dict_commit['author'])
        self.id = dict_commit['id']
        self.parents = dict_commit['parents']
        self.displayId = dict_commit['displayId']
        self.message = dict_commit['message']
        self.authorTimestamp = dict_commit['authorTimestamp']

    def show(self):
        self.author.show()
        print("id =", self.id)
        print("parents =", self.parents)
        print("displayId =", self.displayId)
        print("message =", self.message)
        print("authorTimestamp =", self.authorTimestamp)

    class Author:
        def __init__(self, dict_author):
            self.name = dict_author["name"]
            self.emailAddress = dict_author["emailAddress"]

        def show(self):
            print("author:")
            print("    name         =", self.name)
            print("    emailAddress =", self.emailAddress)
