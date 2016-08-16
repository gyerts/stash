from Library.User import User


class Comment:
    def __init__(self, owner, dict_activity):
        self.owner = owner

        self.id = dict_activity["id"]
        self.createdDate = dict_activity["createdDate"]
        self.user = User(self, dict_activity["user"])
        self.action = dict_activity["action"]
        self.commentAction = dict_activity["commentAction"]
        self.text = dict_activity["comment"]["text"]

    def __str__(self):
        return (self.user.name + ": " + self.text)

    def get_owner(self):
        return self.owner.get_owner() + " -> Comment: id=" + self.id