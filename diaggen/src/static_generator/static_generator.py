import argparse
import os
from .generator_command import GeneratorCommand
from .cpp_translation_unit_extractor import CppTranslationUnitExtractor
from .config import Config
from .puml.static_puml_formatter import StaticPumlFormatter


class StaticGenerator(object):
    def __init__(self, project_root, relative_input_document_path):
        Config.set_class_metadata_extractor(CppTranslationUnitExtractor) # configure dependencies TODO refactor?
        GeneratorCommand.project_root = project_root # TODO refactor this one, yet we don't want to set it on each instance, right?
        self.__input_document_abs_path = os.path.join(project_root, relative_input_document_path)

    def expand_static_generator_cmds(self, output_document_file_path=None):
        if output_document_file_path is None:
            output_document_file_path = self.__input_document_abs_path.replace('.in', '')
        # theoretically, 'w' mode removes content
        # if os.path.isfile(output_document_file_path):
        #     os.remove(output_document_file_path)
        with open(self.__input_document_abs_path) as docfile, open(output_document_file_path, "w") as output_file:
            line = docfile.readline()
            line_number = 1
            while line:
                cmd_parsed, error = GeneratorCommand.try_parse(line)
                if cmd_parsed and not error:
                    parsed_model, error = cmd_parsed.get_model()
                    puml_formatter = StaticPumlFormatter()
                    model_as_string = puml_formatter.get_string(parsed_model)
                    output_file.write('```puml\n')
                    output_file.write(model_as_string)
                    output_file.write('```\n')
                elif not cmd_parsed and not error:  # line was irrelevant for generator...
                    output_file.writelines([line])
                else:
                    print(" === Error in file {} at line {}. === ".format(self.__input_document_abs_path, line_number))
                    print(error)
                line = docfile.readline()
                line_number = line_number + 1
        return output_document_file_path

