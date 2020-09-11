class MethodMetadata(object):
    def __init__(self, name, arguments, return_type):
        self.name = name
        self.return_type_name = return_type
        self.arguments = arguments

    def __repr__(self):
        return "Method name: {}, arguments: {}, return type: {}".format(self.name, self.arguments, self.return_type_name)
