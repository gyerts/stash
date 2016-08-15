from Library.User import User
from Library.File import File


class Commit:
    def __init__(self, url, stash, dict_commit):
        self.stash = stash

        self.id = dict_commit['id']
        self.displayId = dict_commit['displayId']
        self.author = User(dict_commit['author'])
        self.authorTimestamp = dict_commit['authorTimestamp']
        self.message = dict_commit['message']
        self.parents = dict_commit['parents']

        self.url = "%s/commits/%s" % (url, self.id)

        self.files = self.__get_changed_files()

    def __get_changed_files(self):
        response = self.stash.rest_request(self.url + "/changes")["values"]
        files = list()
        for file in response:
            files.append(File(file))
        return files

    def show(self, tab="   "):
        print(tab + "/* --------------------")
        self.author.show(tab)
        print(tab+"id =", self.id)
        print(tab+"parents =", self.parents)
        print(tab+"displayId =", self.displayId)
        print(tab+"message =", self.message)
        print(tab+"authorTimestamp =", self.authorTimestamp)
        print(tab + "files: ")
        for file in self.files:
            print(tab + "   " + file.type + ": " + file.path.name)
        print(tab + "-------------------- */")
