import pytest

from ..src.static_generator.generator_command import GeneratorCommand

def test_generator_command_create_with_ctx_and_ctx_dir():
    with pytest.raises(Exception) as excinfo:
        cmd = GeneratorCommand("test", "ctx", "ctx_dir", "")
    assert "Incorrect static generator command. You can't provide both ctx and ctx-dir." in str(excinfo.value)
