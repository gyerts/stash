from Library.User import User

class Commit:
    def __init__(self, dict_commit):
        self.author = User(dict_commit['author'])
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
