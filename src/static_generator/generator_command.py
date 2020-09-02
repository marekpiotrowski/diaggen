import os
from .config import Config

class GeneratorCommand(object):
    project_root = "/" # TODO refactor this one

    def __init__(self, diagram_identifier, context, context_dir):
        if (context is None and context_dir is None) or (context is not None and context_dir is not None):
            raise Exception("Incorrect static generator command. You can't provide both ctx and ctx-dir.")
        if context_dir is not None:
            context = self.__expand_context_dir(context_dir)
        self.diagram_identifier = diagram_identifier
        self.context = context

    def execute(self):
        translation_units_abs_paths = map(lambda f: os.path.join(self.project_root, f), self.context.split(','))
        TranslationUnitExtractorImpl = Config.get_class_metadata_extractor()
        for translation_unit in translation_units_abs_paths:
            extractor = TranslationUnitExtractorImpl(translation_unit)
            print(extractor.get_classes())

    def __expand_context_dir(self, context_dir):
        abs_directory = os.path.join(self.project_root, context_dir)
        if not os.path.isdir(abs_directory):
            raise Exception("Context directory {} does not exist.".format(abs_directory))
        files = [os.path.join(context_dir, f) for f in os.listdir(abs_directory)]
        return ','.join(files)

    def __repr__(self):
        return "Diagram identifier: {}, context: {}".format(
            self.diagram_identifier, self.context)