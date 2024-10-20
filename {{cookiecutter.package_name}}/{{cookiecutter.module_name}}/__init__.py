"""{{cookiecutter.description}}"""

import importlib.metadata

try:
    __version__ = importlib.metadata.version("{{cookiecutter.module_name}}")
except importlib.metadata.PackageNotFoundError:  # pragma: no cover
    __version__ = "0+unknown"

__all__ = ["__version__"]
