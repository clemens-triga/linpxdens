#read version from installed package
from importlib.metadata import version



from .interactive.session import analyze as analyze
from .core.analysis import analyze as core_analyze

__version__ = version("linpxdens")

__all__ = [
    "analyze",
    "core_analyze",
]
