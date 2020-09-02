class ClassMetadata(object):
    def __init__(self, name, methods = []):
        self.parents = []
        self.name = name
        self.methods = methods
        self.fields = []

    def __repr__(self):
        return "Class {}, methods: {}".format(self.name, self.methods)
