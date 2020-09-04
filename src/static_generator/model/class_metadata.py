class ClassMetadata(object):
    def __init__(self, name, methods, parents):
        self.parents = parents
        self.name = name
        self.methods = methods
        self.fields = []

    def has_method(self, method_name):
        return len(list(filter(lambda m: m == method_name, self.methods))) > 0

    def add_method(self, method_instance):
        self.methods.append(method_instance)

    def add_parent(self, parent_name):
        self.parents.append(parent_name)

    def __repr__(self):
        return "\nClass {}, methods: {}, parents: {}\n".format(self.name, self.methods, self.parents)
