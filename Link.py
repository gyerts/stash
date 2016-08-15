class Link:
    def __init__(self, dict_link):
        self.rel = dict_link['rel']
        self.url = dict_link['url']

    def show(self):
        print('link: ')
        print("      rel =", self.rel)
        print("      url =", self.url)