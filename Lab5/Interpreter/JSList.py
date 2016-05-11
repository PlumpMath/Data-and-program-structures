class JSList:

    def __init__(self):
        self.listan = []


    def __init__(self, lst):
        self.listan = lst


    def length(self):
        return float(len(self.listan))


    def __getitem__(self, key):
        return self.listan[key]


    def __setitem__(self, key, value):
        self.listan[key] = value


    def __str__(self):
        return str(self.listan)

    # Push is the actual JavaScript name,
    # but append was used in the original tests.
    def push(self, this, item):
        self.listan.append(item)
