from importlib import metadata

__version__ = metadata.version(__name__)

from .periodic_table import PeriodicTable, periodic_table  # noqa: F401
from .solvents import solvents  # noqa: F401
