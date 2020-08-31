import argparse
import os


class GeneratorCommand(object):
    project_root = "/" # TODO refactor this one

    def __init__(self, diagram_identifier, context, context_dir):
        if (context is None and context_dir is None) or (context is not None and context_dir is not None):
            raise Exception("Incorrect static generator command. You can't provide both ctx and ctx-dir.")
        if context_dir is not None:
            context = self.__expand_context_dir(context_dir)
        self.diagram_identifier = diagram_identifier
        self.context = context

    def __expand_context_dir(self, context_dir):
        abs_directory = os.path.join(self.project_root, context_dir)
        if not os.path.isdir(abs_directory):
            raise Exception("Context directory {} does not exist.".format(abs_directory))
        files = os.listdir(abs_directory)
        files = list(map(lambda f: os.path.join(context_dir, f), files))
        return ','.join(files)

    def __str__(self):
        return "Diagram identifier: {}, context: {}".format(
            self.diagram_identifier, self.context)


class StaticGenerator(object):
    STATIC_DIAGGEN_TOKEN = "@diaggen-static@"
    OPENING_COMMENT_TOKEN = "<!--"
    CLOSING_COMMENT_TOKEN = "-->"

    def __init__(self, input_document_path, project_root):
        print(input_document_path)
        GeneratorCommand.project_root = project_root # TODO refactor this one, yet we don't want to set it on each instance, right?
        self.__input_document_abs_path = input_document_path
        self.__find_static_generator_cmds()

    def __find_static_generator_cmds(self):
        with open(self.__input_document_abs_path) as docfile:
            line = docfile.readline()
            line_number = 1
            while line:
                if self.STATIC_DIAGGEN_TOKEN in line:
                    try:
                        cmd = self.__parse_static_generator_cmd(line)
                        print(cmd)
                    except Exception as e:
                        print("Error in file {} at line {}.".format(self.__input_document_abs_path, line_number))
                        print(e)
                line = docfile.readline()
                line_number = line_number + 1

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

