import pytest

from ..src.static_generator.generator_command import GeneratorCommand

def test_generator_command_create_with_ctx_and_ctx_dir():
    cmd, error = GeneratorCommand.try_parse("<!-- @diaggen-static@ --id=overall --ctx=api/engine_controller/load_detector.h --ctx-dir=api/engine_controller -->")

    assert "Incorrect static generator command. You can't provide both ctx and ctx-dir." in error
    assert cmd is None
