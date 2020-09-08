import os

class MdWithPumlToPdfGenerator(object):
    def __init__(self):
        pass

    def generate(self, md_file_path):
        temporary_dir_for_files = os.path.dirname(md_file_path)
        print(temporary_dir_for_files)

    def __convert_puml_to_images(self):
        # right now, let's traverse whole file and extract pumls. Later on, we shall optimize it.
        pass
