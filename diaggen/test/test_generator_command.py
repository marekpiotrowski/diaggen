import pytest
import os
import shutil
# from unittest.mock import MagicMock
# from unittest.mock import patch

from ..src.static_generator.generator_command import GeneratorCommand
from ..src.static_generator.config import Config
from ..src.static_generator.model.class_metadata import ClassMetadata
from ..src.static_generator.model.relation import Relation


class DummyTranslationUnitExtractor(object):
    translation_units = []
    abs_includes = []
    ctor_call_count = 0
    get_classes_call_count = 0
    demangle_relations_call_count = 0
    demangle_relations_result = []
    get_classes_result = []

    def __init__(self, translation_unit, abs_includes):
        DummyTranslationUnitExtractor.translation_units.append(translation_unit)
        DummyTranslationUnitExtractor.abs_includes.append(abs_includes)
        DummyTranslationUnitExtractor.ctor_call_count = DummyTranslationUnitExtractor.ctor_call_count + 1

    def get_classes(self):
        DummyTranslationUnitExtractor.get_classes_call_count = DummyTranslationUnitExtractor.get_classes_call_count + 1
        return DummyTranslationUnitExtractor.get_classes_result

    @staticmethod
    def demangle_relations(classes):
        DummyTranslationUnitExtractor.demangle_relations_call_count = DummyTranslationUnitExtractor.demangle_relations_call_count + 1
        return DummyTranslationUnitExtractor.demangle_relations_result

    @staticmethod
    def set_demangle_relations_result(result):
        DummyTranslationUnitExtractor.demangle_relations_result = result

    @staticmethod
    def set_get_classes_result(result):
        DummyTranslationUnitExtractor.get_classes_result = result

    @staticmethod
    def reset():
        DummyTranslationUnitExtractor.translation_units = []
        DummyTranslationUnitExtractor.abs_includes = []
        DummyTranslationUnitExtractor.ctor_call_count = 0
        DummyTranslationUnitExtractor.get_classes_call_count = 0
        DummyTranslationUnitExtractor.demangle_relations_call_count = 0


@pytest.fixture(autouse=True)
def reset_dummies():
    DummyTranslationUnitExtractor.reset()

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

# @patch('..src.static_generator.cpp_translation_unit_extractor.CppTranslationUnitExtractor')
# def test_generator_command_ctx_dir_expands_correctly(DummyTranslationUnitExtractor, create_ctx_dir):
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
    assert DummyTranslationUnitExtractor.get_classes_call_count == 2
    assert DummyTranslationUnitExtractor.demangle_relations_call_count == 1


def test_generator_command_assembles_model_correctly(create_ctx_dir):
    # given
    Config.set_class_metadata_extractor(DummyTranslationUnitExtractor)
    classes_result = [ClassMetadata("Class1", [], parents=[]), ClassMetadata("Class2", [], parents=[])]
    relations_result = [Relation("Class1", "Class2", Relation.INHERITANCE)]
    DummyTranslationUnitExtractor.set_demangle_relations_result(relations_result)
    DummyTranslationUnitExtractor.set_get_classes_result(classes_result)
    GeneratorCommand.project_root = os.getcwd()

    # when
    cmd, error = GeneratorCommand.try_parse("<!-- @diaggen-static@ --id=overall --ctx=example_ctx_dir/header1.h -->")
    assert error is None
    model = cmd.get_model()

    # then
    assert model.classes == classes_result
    assert model.relations == relations_result
    assert DummyTranslationUnitExtractor.ctor_call_count == 1
    assert DummyTranslationUnitExtractor.get_classes_call_count == 1
    assert DummyTranslationUnitExtractor.demangle_relations_call_count == 1