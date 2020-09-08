import os
import re

class MdWithPumlToPdfGenerator(object):
    def __init__(self):
        pass

    def generate(self, md_file_path):
        temporary_dir_for_files = os.path.dirname(md_file_path)
        with open(md_file_path, 'r') as md_file:
            content = md_file.read()
        self.__convert_puml_to_images(content)
        print(temporary_dir_for_files)

    @staticmethod
    def __convert_puml_to_images(md_file_contents):
        # right now, let's traverse whole file and extract pumls. Later on, we shall optimize it.
        # todo fix regex
        puml_regexp = re.compile(r"```(.*)+```$", re.MULTILINE)
        # right now, let's traverse whole file and extract pumls. Later on, we shall optimize it.
        umls = puml_regexp.findall(md_file_contents)
        print(umls)
