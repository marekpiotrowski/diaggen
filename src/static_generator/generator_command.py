import os
from .config import Config

class GeneratorCommand(object):
    project_root = "/" # TODO refactor this one

    def __init__(self, diagram_identifier, context, context_dir, relative_includes):
        if (context is None and context_dir is None) or (context is not None and context_dir is not None):
            raise Exception("Incorrect static generator command. You can't provide both ctx and ctx-dir.")
        if context_dir is not None:
            context = self.__expand_context_dir(context_dir)
        self.diagram_identifier = diagram_identifier
        self.context = context
        self.relative_includes = "" if relative_includes is None else relative_includes

    def execute(self):
        translation_units_abs_paths = map(lambda f: os.path.join(self.project_root, f), self.context.split(','))
        abs_includes = [os.path.join(self.project_root, incl) for incl in self.relative_includes.split(',')]
        TranslationUnitExtractorImpl = Config.get_class_metadata_extractor()
        all_classes_grouped = {}
        for translation_unit in translation_units_abs_paths:
            extractor = TranslationUnitExtractorImpl(translation_unit, abs_includes)
            for c in extractor.get_classes():
                if c.name not in all_classes_grouped:
                    all_classes_grouped[c.name] = [c]
                else:
                    all_classes_grouped[c.name].append(c)
        self.__synthesize_classes_from_multiple_units(all_classes_grouped)

    def __synthesize_classes_from_multiple_units(self, classes):
        result = {}
        for class_id, classes in classes.items():
            most_detailed = None
            for c in classes:
                most_detailed = c.get_more_detailed(most_detailed)
            result[class_id] = most_detailed
        print(list(result.values()))
        return list(result.values())


    def __expand_context_dir(self, context_dir):
        abs_directory = os.path.join(self.project_root, context_dir)
        if not os.path.isdir(abs_directory):
            raise Exception("Context directory {} does not exist.".format(abs_directory))
        files = [os.path.join(context_dir, f) for f in os.listdir(abs_directory)]
        return ','.join(files)

    def __repr__(self):
        return "Diagram identifier: {}, context: {}".format(
            self.diagram_identifier, self.context)