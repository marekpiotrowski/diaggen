import os
import argparse
from .config import Config
from .model.class_diagram_model import ClassDiagramModel

class GeneratorCommand(object):
    project_root = "/" # TODO refactor this one
    STATIC_DIAGGEN_TOKEN = "@diaggen-static@"
    OPENING_COMMENT_TOKEN = "<!--"
    CLOSING_COMMENT_TOKEN = "-->"

    def __init__(self, diagram_identifier, context, relative_includes):
        self.__diagram_identifier = diagram_identifier
        self.__context = context
        self.__relative_includes = "" if relative_includes is None else relative_includes

    def get_model(self):
        translation_units_abs_paths = map(lambda f: os.path.join(self.project_root, f), self.__context.split(','))
        abs_includes = [os.path.join(self.project_root, incl) for incl in self.__relative_includes.split(',')]
        TranslationUnitExtractorImpl = Config.get_class_metadata_extractor()
        all_classes_grouped = {}
        for translation_unit in translation_units_abs_paths:
            extractor = TranslationUnitExtractorImpl(translation_unit, abs_includes)
            for c in extractor.get_classes():
                if c.name not in all_classes_grouped:
                    all_classes_grouped[c.name] = [c]
                else:
                    all_classes_grouped[c.name].append(c)
        classes_big_picture = self.__synthesize_classes_from_multiple_units(all_classes_grouped)
        relations = TranslationUnitExtractorImpl.demangle_relations(classes_big_picture)
        model = ClassDiagramModel(classes_big_picture, relations)
        return model

    @staticmethod
    def __synthesize_classes_from_multiple_units(classes):
        result = {}
        for class_id, classes in classes.items():
            most_detailed = None
            for c in classes:
                if c.is_more_detailed_than(most_detailed):
                    most_detailed = c
            result[class_id] = most_detailed
        return list(result.values())

    @staticmethod
    def __expand_context_dir(context_dir):
        abs_directory = os.path.join(GeneratorCommand.project_root, context_dir)
        if not os.path.isdir(abs_directory):
            raise Exception("Context directory {} does not exist.".format(abs_directory))
        files = [os.path.join(context_dir, f) for f in os.listdir(abs_directory)]
        return ','.join(files)

    @staticmethod
    def try_parse(line):
        if GeneratorCommand.STATIC_DIAGGEN_TOKEN not in line:
            return None, None
        line = line.replace(GeneratorCommand.OPENING_COMMENT_TOKEN, ''). \
            replace(GeneratorCommand.CLOSING_COMMENT_TOKEN, '')
        parser = argparse.ArgumentParser(description='Static diaggen parser.')
        parser.add_argument("--id", help='Diagram unique identifier.')
        parser.add_argument("--ctx", help='Context (file list) for diagram generation.')
        parser.add_argument("--ctx-dir", help='Context (directory) for diagram generation.')
        parser.add_argument("--includes", help='Comma-separated list of relative include directories used for compilation.')
        args = parser.parse_known_args(line.split(" "))
        known_args = args[0]
        if (known_args.ctx is None and known_args.ctx_dir is None) or (known_args.ctx is not None and known_args.ctx_dir is not None):
            return None, "Incorrect static generator command. You can't provide both ctx and ctx-dir."
        context = known_args.ctx
        if known_args.ctx_dir is not None:
            try:
                context = GeneratorCommand.__expand_context_dir(known_args.ctx_dir)
            except Exception as e:
                return None, str(e)
        cmd = GeneratorCommand(known_args.id, context, known_args.includes)
        return cmd, None

    def __repr__(self):
        return "Diagram identifier: {}, context: {}".format(
            self.__diagram_identifier, self.__context)
