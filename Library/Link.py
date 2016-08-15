class Link:
    def __init__(self, dict_link):
        self.rel = dict_link['rel']
        self.url = dict_link['url']

    def show(self, tab="   "):
        print(tab + 'link: ')
        print(tab + "   rel =", self.rel)
        print(tab + "   url =", self.url)
