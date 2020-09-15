import pytest
import os
import shutil

from ..src.static_generator.generator_command import GeneratorCommand
from ..src.static_generator.config import Config


class DummyTranslationUnitExtractor(object):
    translation_units = []
    abs_includes = []
    ctor_call_count = 0

    def __init__(self, translation_unit, abs_includes):
        DummyTranslationUnitExtractor.translation_units.append(translation_unit)
        DummyTranslationUnitExtractor.abs_includes.append(abs_includes)
        DummyTranslationUnitExtractor.ctor_call_count = DummyTranslationUnitExtractor.ctor_call_count + 1

    def get_classes(self):
        return []

    @staticmethod
    def demangle_relations(classes):
        return []

@pytest.fixture()
def create_ctx_dir():
    ctx_dir_path = os.path.join(os.getcwd(), 'example_ctx_dir')
    os.mkdir(ctx_dir_path)
    f1 = open(os.path.join(ctx_dir_path, "header1.h"), 'w')
    f2 = open(os.path.join(ctx_dir_path, "header2.h"), 'w')
    f1.close()
    f2.close()
    yield
    shutil.rmtree(ctx_dir_path)


def test_generator_command_create_with_ctx_and_ctx_dir():
    cmd, error = GeneratorCommand.try_parse("<!-- @diaggen-static@ --id=overall --ctx=api/engine_controller/load_detector.h --ctx-dir=api/engine_controller -->")

    assert "Incorrect static generator command. You can't provide both ctx and ctx-dir." in error
    assert cmd is None


def test_generator_command_ctx_dir_does_not_exist():
    non_existing_dir = os.path.join(os.getcwd(), '/nonexistingdir')
    GeneratorCommand.project_root = non_existing_dir
    cmd, error = GeneratorCommand.try_parse("<!-- @diaggen-static@ --id=overall --ctx-dir=some_api -->")

    assert "Context directory {} does not exist.".format(os.path.join(non_existing_dir, 'some_api')) in error
    assert cmd is None


def test_generator_command_ctx_dir_expands_correctly(create_ctx_dir):
    Config.set_class_metadata_extractor(DummyTranslationUnitExtractor)
    GeneratorCommand.project_root = os.getcwd()
    cmd, error = GeneratorCommand.try_parse("<!-- @diaggen-static@ --id=overall --ctx-dir=example_ctx_dir -->")

    assert error is None

    model = cmd.get_model()

    h1 = os.path.join(GeneratorCommand.project_root, 'example_ctx_dir', 'header1.h')
    h2 = os.path.join(GeneratorCommand.project_root, 'example_ctx_dir', 'header2.h')
    assert model.classes == []
    assert model.relations == []
    assert h1 in DummyTranslationUnitExtractor.translation_units and h2 in DummyTranslationUnitExtractor.translation_units
    assert DummyTranslationUnitExtractor.ctor_call_count == 2