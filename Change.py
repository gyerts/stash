from collections import OrderedDict

class Change:
    def __init__(self, owner):
        self.owner = owner

        self.change = None
        self.date = None
        self.review = ''
        self.reviewed = ''
        self.author = None
        self.domain = None
        self.state = None
        self.reviewers = list()
        self.files = list()
        self.formats = set()
        self.comments = list()
        self.comments_text = list()
        self.time_spent = None

    def get_owner(self):
        return self.owner.get_owner() + " -> Change"

    def to_dict(self):
        output = OrderedDict()

        output["change"] = self.change
        output["date"] = self.date
        output["review"] = self.review
        output["reviewed"] = self.reviewed
        output["author"] = self.author
        output["domain"] = self.domain
        output["state"] = self.state
        output["reviewers"] = self.reviewers
        output["files"] = self.files
        output["formats"] = list(self.formats)
        output["comments"] = self.comments
        output["comments_text"] = self.comments_text
        output["time_spent"] = self.time_spent

        return output

    def show(self, tab="   "):
        print(tab, "/* --------------------------")
        print(tab, {"change":self.change})
        print(tab, {"date":self.date})
        print(tab, {"review":self.review})
        print(tab, {"reviewed":self.reviewed})
        print(tab, {"author":self.author})
        print(tab, {"domain":self.domain})
        print(tab, {"state":self.state})
        print(tab, {"reviewers":self.reviewers})
        print(tab, {"files":self.files})
        print(tab, {"formats":list(self.formats)})
        print(tab, {"comments":self.comments})
        print(tab, {"comments_text":self.comments_text})
        print(tab, {"time_spent":self.time_spent})
        print(tab, "-------------------------- */")
