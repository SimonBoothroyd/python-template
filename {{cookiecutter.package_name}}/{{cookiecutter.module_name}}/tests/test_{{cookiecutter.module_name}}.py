import importlib


def test_{{cookiecutter.module_name}}():
    assert importlib.import_module("{{cookiecutter.module_name}}") is not None
