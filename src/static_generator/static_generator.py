import argparse
import os
from .generator_command import GeneratorCommand
from .cpp_translation_unit_extractor import CppTranslationUnitExtractor
from .config import Config


class StaticGenerator(object):
    STATIC_DIAGGEN_TOKEN = "@diaggen-static@"
    OPENING_COMMENT_TOKEN = "<!--"
    CLOSING_COMMENT_TOKEN = "-->"

    def __init__(self, project_root, relative_input_document_path):
        Config.set_class_metadata_extractor(CppTranslationUnitExtractor) # configure dependencies TODO refactor?
        GeneratorCommand.project_root = project_root # TODO refactor this one, yet we don't want to set it on each instance, right?
        self.__input_document_abs_path = os.path.join(project_root, relative_input_document_path)
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
                        cmd.execute()
                    except Exception as e:
                        print(" === Error in file {} at line {}. === ".format(self.__input_document_abs_path, line_number))
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
        parser.add_argument("--includes", help='Comma-separated list of relative include directories used for compilation.')
        args = parser.parse_known_args(line.split(" "))
        known_args = args[0]
        cmd = GeneratorCommand(known_args.id, known_args.ctx, known_args.ctx_dir, known_args.includes)
        return cmd

