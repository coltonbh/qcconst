"""Solvent data model.

References:
    - Dielectric constants: <https://depts.washington.edu/eooptic/linkfiles/dielectric_chart%5B1%5D.pdf>
"""

import csv
from dataclasses import dataclass
from pathlib import Path

from .utils import to_table


@dataclass(frozen=True)
class Solvent:
    """Solvent data model."""

    name: str
    dielectric: float
    sources: list[str]


class SolventDict(dict):
    """Custom dictionary for solvents with extra convenience methods."""

    def as_list(self):
        """Return a list of all solvents."""
        return list(self.keys())

    def show(self):
        """Print a human-readable table of solvents and their dielectric constants."""
        to_table(list(self.values()))


solvents = SolventDict()


def _load_solvents(csv_path: Path):
    """Load solvents from CSV into the SOLVENTS dictionary."""
    with csv_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            dielectric = float(row["dielectric"])
            sources = row["sources"].split(",")
            solvents[name] = Solvent(name=name, dielectric=dielectric, sources=sources)


# Load on import
_load_solvents(Path(__file__).parent / "data" / "solvents.csv")
