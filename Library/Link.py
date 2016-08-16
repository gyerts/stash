class Link:
    def __init__(self, owner, dict_link):
        self.owner = owner

        self.rel = dict_link['rel']
        self.url = dict_link['url']

    def show(self, tab="   "):
        print(tab + 'link: ')
        print(tab + "   rel =", self.rel)
        print(tab + "   url =", self.url)

    def get_owner(self):
        return self.owner.get_owner() + " -> Link"