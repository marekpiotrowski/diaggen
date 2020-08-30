
class StaticGenerator(object):
    def __init__(self, input_document_abs_path):
        print(input_document_abs_path)
        self.__input_document_abs_path = input_document_abs_path
        self.__find_static_generator_cmds()

    def __find_static_generator_cmds(self):
        with open(self.__input_document_abs_path) as docfile:
            line = docfile.readline()
            while line:
                print(line.strip())
                # TODO do something with line
                line = docfile.readline()
