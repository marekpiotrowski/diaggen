class ClassMetadata(object):
    def __init__(self, name):
        self.parents = []
        self.name = name
        self.methods = []
        self.fields = []

    def __repr__(self):
        return "Class {}".format(self.name)
