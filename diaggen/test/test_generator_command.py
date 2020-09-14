import pytest
import os
import shutil

from ..src.static_generator.generator_command import GeneratorCommand


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
    GeneratorCommand.project_root = os.getcwd()
    cmd, error = GeneratorCommand.try_parse("<!-- @diaggen-static@ --id=overall --ctx-dir=example_ctx_dir -->")

    assert error is None
    h1 = os.path.join('example_ctx_dir', 'header1.h')
    h2 = os.path.join('example_ctx_dir', 'header2.h')
    assert cmd.context == ",".join([h1, h2]) or cmd.context == ",".join([h2, h1])