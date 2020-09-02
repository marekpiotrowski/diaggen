class MethodMetadata(object):
    def __init__(self, name):
        self.name = name
        self.return_type_name = None
        self.arguments = None

    def __repr__(self):
        return "Method name: {}".format(self.name)
