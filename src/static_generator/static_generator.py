import argparse


class GeneratorCommand(object):
    def __init__(self, diagram_identifier, context, context_dir):
        self.diagram_identifier = diagram_identifier
        self.context = context
        self.context_dir = context_dir

    def __str__(self):
        return "Diagram identifier: {}, context: {}, context directory: {}".format(
            self.diagram_identifier, self.context, self.context_dir)


class StaticGenerator(object):
    STATIC_DIAGGEN_TOKEN = "@diaggen-static@"
    OPENING_COMMENT_TOKEN = "<!--"
    CLOSING_COMMENT_TOKEN = "-->"

    def __init__(self, input_document_abs_path):
        print(input_document_abs_path)
        self.__input_document_abs_path = input_document_abs_path
        self.__find_static_generator_cmds()

    def __find_static_generator_cmds(self):
        with open(self.__input_document_abs_path) as docfile:
            line = docfile.readline()
            while line:
                if self.STATIC_DIAGGEN_TOKEN in line:
                    cmd = self.__parse_static_generator_cmd(line)
                    print(cmd)
                line = docfile.readline()

    def __parse_static_generator_cmd(self, line):
        line = line.replace(self.OPENING_COMMENT_TOKEN, ''). \
            replace(self.CLOSING_COMMENT_TOKEN, '')
        parser = argparse.ArgumentParser(description='Static diaggen parser.')
        parser.add_argument("--id", help='Diagram unique identifier.')
        parser.add_argument("--ctx", help='Context (file list) for diagram generation.')
        parser.add_argument("--ctx-dir", help='Context (directory) for diagram generation.')
        args = parser.parse_known_args(line.split(" "))
        known_args = args[0]
        cmd = GeneratorCommand(known_args.id, known_args.ctx, known_args.ctx_dir)
        return cmd

