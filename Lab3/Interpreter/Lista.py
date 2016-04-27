class Lista:

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
