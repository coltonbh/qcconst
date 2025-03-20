"""Physical constants from NIST CODATA 2022 and PubChem. All values must have a reference to their source.

References:
    - <https://physics.nist.gov/cuu/Constants/Table/allascii.txt>
"""

import csv
import inspect
import sys
from pathlib import Path

from .utils import to_table


class Constant(float):
    """A float subclass holding additional metadata."""

    unit: str
    source: str
    notes: str

    def __new__(cls, value, unit: str, source: str, notes: str):
        obj = float.__new__(cls, value)
        obj.unit = unit
        obj.source = source
        obj.notes = notes
        return obj

    def __repr__(self):
        return f"{float(self)}, unit={self.unit}, source={self.source} {'notes=' + self.notes if self.notes else ''}"


def _load_constants(csv_path: Path):
    """Load constants from CSV and set as module attributes."""
    current_module = sys.modules[__name__]
    with csv_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            value = float(row["value"])
            unit = row["unit"]
            source = row["source"]
            notes = row["notes"]
            setattr(current_module, name, Constant(value, unit, source, notes))


# Load constants at import time
_load_constants(Path(__file__).parent / "data" / "constants.csv")


def as_list():
    """Return a list of all defined constants."""
    current_module = sys.modules[__name__]
    return [
        name
        for name, value in inspect.getmembers(current_module)
        if name.isupper()
        and not inspect.ismodule(value)
        and not inspect.isfunction(value)
    ]


def show():
    """Print a human-readable table of all constants."""
    current_module = sys.modules[__name__]
    constants_list = []
    for name in as_list():
        constant = getattr(current_module, name)
        constants_list.append(
            {
                "name": name,
                "value": float(constant),
                "unit": constant.unit,
                "source": constant.source,
            }
        )
    to_table(constants_list)


def _sources():
    """List unique sources for constants and conversion factors."""
    current_module = sys.modules[__name__]
    unique_sources = set()

    for name in as_list():
        source = getattr(current_module, name).source
        if not source.startswith("Derived"):
            unique_sources.add(source)

    return sorted(unique_sources)


sources = _sources()
