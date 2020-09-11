import os
import re

import subprocess

class MdWithPumlToPdfGenerator(object):
    IMG_EXTENSION = "png"
    PUML_EXTENSION = "puml"
    TEMPLATE_BASE = "diagram"

    def __init__(self):
        self.__temporary_dir_for_files = None

    def generate(self, md_file_path):
        self.__temporary_dir_for_files = os.path.dirname(md_file_path)
        output_file_path = md_file_path.replace('.', '_with_img.')
        with open(md_file_path, 'r') as md_file:
            content = md_file.read()
        images_paths = self.__prepare_images(content)
        puml_idx = 0
        ignore = False
        with open(md_file_path, 'r') as md_file, open(output_file_path, 'w') as output_file:
            while True:
                line = md_file.readline()
                if line == '':  #EOF
                    break
                if '```' in line and ignore:
                    ignore = False
                    continue
                if ignore:
                    continue
                if '```puml' in line:
                    # todo implicitly assume name!
                    line = '![Diagram {}]({}{}.{})\n\n'.format(puml_idx, self.TEMPLATE_BASE, puml_idx, self.IMG_EXTENSION)
                    output_file.writelines([line])
                    puml_idx = puml_idx + 1
                    ignore = True
                    continue
                output_file.writelines([line])

    def __save_puml_to_file(self, puml, idx):
        abs_file_path = os.path.join(self.__temporary_dir_for_files, "{}{}.{}".format(self.TEMPLATE_BASE, idx, self.PUML_EXTENSION))
        with open(abs_file_path, "w") as puml_file:
            puml_file.write(puml)
        return abs_file_path

    def __convert_puml_to_img(self, puml_file_path):
        # TODO this one is not portable!
        subprocess.run(["plantuml", puml_file_path])
        return puml_file_path.replace('.{}'.format(self.PUML_EXTENSION), '.{}'.format(self.IMG_EXTENSION))

    def __prepare_images(self, md_file_contents):
        # right now, let's traverse whole file and extract pumls. Later on, we shall optimize it.
        puml_regexp = re.compile(r"```puml\n((.+\n)+?)```", re.MULTILINE)
        umls = puml_regexp.findall(md_file_contents)
        umls_flat = [u[0] for u in umls]
        diagram_idx = 0
        images_paths = []
        for puml in umls_flat:
            puml_file_path = self.__save_puml_to_file(puml, diagram_idx)
            img_file_path = self.__convert_puml_to_img(puml_file_path)
            images_paths.append(img_file_path)
            diagram_idx = diagram_idx + 1
        return images_paths
