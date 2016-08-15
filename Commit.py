from Library.User import User

class Commit:
    def __init__(self, dict_commit):
        self.id = dict_commit['id']
        self.displayId = dict_commit['displayId']
        self.author = User(dict_commit['author'])
        self.authorTimestamp = dict_commit['authorTimestamp']
        self.message = dict_commit['message']
        self.parents = dict_commit['parents']

    def show(self, tab="   "):
        print(tab + "/* --------------------")
        self.author.show(tab)
        print(tab+"id =", self.id)
        print(tab+"parents =", self.parents)
        print(tab+"displayId =", self.displayId)
        print(tab+"message =", self.message)
        print(tab+"authorTimestamp =", self.authorTimestamp)
        print(tab + "-------------------- */")
