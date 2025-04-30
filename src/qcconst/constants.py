"""Physical constants from NIST CODATA 2022 and PubChem. All values must have a reference to their source.

Developer Notes:
    - The constants are loaded from a csv file and set as module attributes.
    - The `Constant` class is a subclass of `float` that holds additional metadata.
    - The `as_list` function returns a list of all defined constants.
    - The `show` function prints a human-readable table of all constants.
    - The `sources` list contains all sources for constants and conversion factors.
    - I considered subclassing dict for a ConstantsDict so that it has typical .keys(), .values(), and .items() methods.
        However, I decided against it because one looses IDE autocompletion for the constants as module-level attributes,
        which is more convenient for users.

References:
    - <https://physics.nist.gov/cuu/Constants/Table/allascii.txt>
"""

import csv
import inspect
import sys
from pathlib import Path
from typing import Optional

from .models import Value
from .utils import to_table

# For auto-completion in IDEs
__all__ = []  # filled by _load_constants and _load_codata


def _load_constants(csv_path: Path):
    """Load constants from csv and set as module attributes."""
    current_module = sys.modules[__name__]
    with csv_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            value = float(row["value"])
            unit = row["unit"]
            source = row["source"]
            uncertainty = float(row["uncertainty"]) if row["uncertainty"] else None
            notes = row["notes"]
            setattr(
                current_module, name, Value(value, unit, source, uncertainty, notes)
            )
            __all__.append(name)  # Add the name to the module's __all__ list


def _load_codata(year: int):
    """Load CODATA constants from a csv file."""
    codata_path = Path(__file__).parent / "data" / f"codata{year}.csv"

    def _process_float(value: str) -> Optional[float]:
        """Handle CODATA's spaces and ellipses in float values."""
        return float(row["value"].replace(" ", "").replace("...", ""))

    codata = {}
    with codata_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["quantity"]
            # Remove spaces and ellipses from the value
            value = _process_float(row["value"])
            uncertainty = (
                _process_float(row["uncertainty"])
                if row["uncertainty"] != "(exact)"
                else 0.0
            )
            unit = row["unit"]
            source = f"CODATA {year}: https://physics.nist.gov/cuu/Constants/Table/allascii.txt"
            codata[name] = Value(
                value, unit, source, uncertainty=uncertainty, notes=""
            )

    # Set the codata attribute in the module
    current_module = sys.modules[__name__]
    setattr(current_module, f"codata{year}", codata)
    # Add the names to the module's __all__ list
    __all__.append(f"codata{year}")


# Load constants at import time
_load_constants(Path(__file__).parent / "data" / "constants.csv")
_load_codata(2022)  # CODATA 2022 constants
phys = getattr(sys.modules[__name__], "codata2022")  # Alias for the CODATA 2022 constants

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
                "uncertainty": constant.uncertainty,
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


def __dir__():
    """Override the default dir() to show only constants and dunder methods."""
    # This is a workaround to avoid showing all module attributes in the tab-completion.
    return __all__ + [n for n in globals() if n.startswith("__") and n.endswith("__")]
