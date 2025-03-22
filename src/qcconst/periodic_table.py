"""A Periodic Table from PubChem data. Other data may be used to instantiate a Periodic Table too.
All values must have a reference to their source.

References:
    - PubChem periodic table data: <https://pubchem.ncbi.nlm.nih.gov/periodic-table/>. Click "Download"
        to get the CSV file.
"""

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from .utils import to_table


@dataclass(frozen=True)
class Atom:
    """Atom data model."""

    symbol: str
    number: int
    name: str
    mass: float
    group: Optional[int]
    period: int
    block: str
    electron_config: str


class PeriodicTable:
    """Periodic table data model. Data source and URL should be set by class methods."""

    # Should be set by @classmethod
    sources: List[str]

    @classmethod
    def from_pubchem(cls):
        """Create a periodic table from PubChem data."""
        instance = cls()
        instance.sources = [
            "https://pubchem.ncbi.nlm.nih.gov/periodic-table",
            "https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV?response_type=save&response_basename=PubChemElements_all",
        ]

        group_and_period_data = {}

        data_dir = Path(__file__).parent / "data"

        with open(data_dir / "group_period.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                group_and_period_data[row["Symbol"]] = {
                    "group": int(row["Group"]) if row["Group"] else None,
                    "period": int(row["Period"]),
                }

        with open(data_dir / "pubchem.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                symbol = row["Symbol"]
                atom = Atom(
                    symbol=symbol,
                    number=int(row["AtomicNumber"]),
                    name=row["Name"],
                    mass=float(row["AtomicMass"]),
                    group=group_and_period_data[symbol]["group"],
                    period=group_and_period_data[symbol]["period"],
                    block=row["GroupBlock"],
                    electron_config=row["ElectronConfiguration"],
                )
                setattr(instance, symbol, atom)
        return instance

    def group(self, group_number: int) -> list[Atom]:
        """Return all atoms in a group."""
        assert 1 <= group_number <= 18, "Group number must be between 1 and 18."
        return [
            atom
            for atom in self.__dict__.values()
            if isinstance(atom, Atom) and atom.group == group_number
        ]

    def period(self, period_number: int) -> list[Atom]:
        """Return all atoms in a period."""
        assert 1 <= period_number <= 7, "Period number must be between 1 and 7."
        return [
            atom
            for atom in self.__dict__.values()
            if isinstance(atom, Atom) and atom.period == period_number
        ]

    def number(self, number: int) -> Atom:
        """Return an atom by atomic number."""
        for atom in self.__dict__.values():
            if isinstance(atom, Atom) and atom.number == number:
                return atom
        raise ValueError(f"No atom with atomic number {number}.")

    def show(self):
        """Print all atoms in a human-readable format."""
        print(f"Sources: {', '.join(self.sources)}\n")
        to_table([val for val in self.__dict__.values() if isinstance(val, Atom)])


periodic_table = PeriodicTable.from_pubchem()
"""Periodic table data from PubChem.

    Attributes:
        data_source (str): Data source.
        data_url (str): Data URL.

    Example:
        ```python
        >>> from qcconst import periodic_table as pt
        
        >>> pt.Ni
        Atom(symbol='Ni', number=28, name='Nickel', mass=58.6934, group=10, period=4, block='d', electron_config='[Ar] 3d8 4s2')

        >>> pt.group(1)
        [Atom(symbol='H', number=1, name='Hydrogen', mass=1.00784, group=1, period=1, block='s', electron_config='1s1'),  # noqa: E501
        Atom(symbol='Li', number=3, name='Lithium', mass=6.94, group=1, period=2, block='s', electron_config='[He] 2s1'),  # noqa: E501
        Atom(symbol='Na', number=11, name='Sodium', mass=22.98976928, group=1, period=3, block='s', electron_config='[Ne] 3s1'),  # noqa: E501
        Atom(symbol='K', number=19, name='Potassium', mass=39.0983, group=1, period=4, block='s', electron_config='[Ar] 4s1'),  # noqa: E501
        Atom(symbol='Rb', number=37, name='Rubidium', mass=85.4678, group=1, period=5, block='s', electron_config='[Kr] 5s1'),  # noqa: E501
        Atom(symbol='Cs', number=55, name='Cesium', mass=132.90545196, group=1, period=6, block='s', electron_config='[Xe] 6s1'),  # noqa: E501
        Atom(symbol='Fr', number=87, name='Francium', mass=223.0, group=1, period=7, block='s', electron_config='[Rn] 7s1')]  # noqa: E501
        ```
"""
