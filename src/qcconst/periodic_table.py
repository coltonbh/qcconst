"""A Periodic Table. All values must have a reference to their source.

References:
    - PubChem periodic table data: <https://pubchem.ncbi.nlm.nih.gov/periodic-table>. Click "Download"
        to get the CSV file.
    - Covalent radii from Cordero et. al. 2008: <https://doi.org/10.1039/b801115j>.
      - The CRC Handbook takes the average of Cordero et. al. 2008 and Pyykkö et al., 2009 as its
        reference values for covalent radii as per
        <https://github.com/python-periodictable/periodictable/blob/master/periodictable/covalent_radius.py>.
        For now we are just going with Cordero for simplicity.
    - van der Wall radii from Alvarez 2013: <https://doi.org/10.1039/C3DT50599E>.
"""

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from . import constants
from .models import Value
from .utils import to_table


@dataclass(frozen=True)
class Element:
    """Atom data model."""

    symbol: str
    number: int
    name: str
    mass: Value
    group: Optional[int]
    period: int
    block: str
    electron_config: str
    electronegativity: Optional[Value]
    atomic_radius: Value
    cov_radius: Optional[Value]
    cov_radius_double: Optional[Value]
    cov_radius_triple: Optional[Value]
    vdw_radius: Optional[Value]


class PeriodicTable:
    """Periodic table data model. Data source and URL should be set by class methods."""

    @classmethod
    def from_data(cls):
        """Create a periodic table from PubChem data."""
        instance = cls()
        element_data = {}
        data_dir = Path(__file__).parent / "data"

        # Load group and period data
        with open(data_dir / "group_period.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                element_data[row["Symbol"]] = {
                    "group": int(row["Group"]) if row["Group"] else None,
                    "period": int(row["Period"]),
                }

        # Load Cordero covalent radius data
        with open(data_dir / "covalent_radii_cordero_2008.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                symbol = row["symbol"]
                notes = ""

                # Just use Csp3 for carbon
                if symbol == "Csp3":
                    symbol = "C"
                    sp2_row = next(reader)
                    sp_row = next(reader)
                    notes = f"Using sp3 hybridized carbon. sp2 and sp hybridized carbon are {float(sp2_row['cov_radius']) * constants.ANGSTROM_TO_BOHR} and {float(sp_row['cov_radius']) * constants.ANGSTROM_TO_BOHR} Bohr respectively."

                # Use low spin values for Mn, Fe, Co
                if "l.s." in symbol:
                    symbol = symbol.replace(" l.s.", "")
                    hs_row = next(reader)
                    notes = f"Using low spin value for {symbol}. High spin value is {float(hs_row['cov_radius']) * constants.ANGSTROM_TO_BOHR} Bohr."

                cov_radius = Value(
                    float(row["cov_radius"]) * constants.ANGSTROM_TO_BOHR,
                    unit="Bohr",
                    source="Cordero et al. 2008: https://doi.org/10.1039/b801115j",
                    uncertainty=float(row["est_std_dev"])
                    * 0.01
                    * constants.ANGSTROM_TO_BOHR
                    if row["est_std_dev"]
                    else None,
                    notes=notes,
                )
                element_data[symbol]["cov_radius"] = cov_radius

        # Load Pyykkö covalent radius data
        with open(data_dir / "covalent_radii_pyykko_2009.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                symbol = row["symbol"]
                cov_radius_double = (
                    Value(
                        float(row["r2"]) / 100 * constants.ANGSTROM_TO_BOHR,
                        unit="Bohr",
                        source="Pyykkö et al. 2009: https://doi.org/10.1002/chem.200901472",
                        uncertainty=None,
                        notes="",
                    )
                    if row["r2"]
                    else None
                )
                cov_radius_triple = (
                    Value(
                        float(row["r3"]) / 100 * constants.ANGSTROM_TO_BOHR,
                        unit="Bohr",
                        source="Pyykkö et al. 2009: https://doi.org/10.1002/chem.200901472",
                        uncertainty=None,
                        notes="",
                    )
                    if row["r3"]
                    else None
                )
                element_data[symbol]["cov_radius_double"] = cov_radius_double
                element_data[symbol]["cov_radius_triple"] = cov_radius_triple
        # Load van der Waals radius data
        with open(data_dir / "vdw_radii_alvarez_2013.csv") as file:
            reader = csv.DictReader(file)
            for row in reader:
                symbol = row["symbol"]
                vdw_radius = Value(
                    float(row["vdw_radius"].translate(str.maketrans("", "", "[]")))
                    * constants.ANGSTROM_TO_BOHR,
                    unit="Bohr",
                    source="Alvarez 2013: https://doi.org/10.1039/C3DT50599E",
                    uncertainty=None,
                    notes=row["notes"],
                )
                element_data[symbol]["vdw_radius"] = vdw_radius

        # Load PubChem data and create Element instances
        with open(data_dir / "pubchem.csv") as file:
            reader = csv.DictReader(file)
            pubchem_source = "PubChem: https://pubchem.ncbi.nlm.nih.gov/periodic-table"
            for row in reader:
                symbol = row["Symbol"]
                atom = Element(
                    symbol=symbol,
                    number=int(row["AtomicNumber"]),
                    name=row["Name"],
                    mass=Value(
                        row["AtomicMass"],
                        "amu",
                        pubchem_source,
                        None,
                        "",
                    ),
                    group=element_data[symbol]["group"],
                    period=element_data[symbol]["period"],
                    block=row["GroupBlock"],
                    electron_config=row["ElectronConfiguration"],
                    electronegativity=Value(
                        row["Electronegativity"],
                        "Pauling",
                        pubchem_source,
                        None,
                        "",
                    )
                    if row["Electronegativity"]
                    else None,
                    atomic_radius=Value(
                        float(row["AtomicRadius"]) / 100 * constants.ANGSTROM_TO_BOHR,
                        "Bohr",
                        pubchem_source,
                        None,
                        "",
                    )
                    if row["AtomicRadius"]
                    else None,
                    cov_radius=element_data[symbol].get("cov_radius"),
                    cov_radius_double=element_data[symbol].get("cov_radius_double"),
                    cov_radius_triple=element_data[symbol].get("cov_radius_triple"),
                    vdw_radius=element_data[symbol].get("vdw_radius"),
                )
                setattr(instance, symbol, atom)
        return instance

    def group(self, group_number: int) -> list[Element]:
        """Return all atoms in a group."""
        assert 1 <= group_number <= 18, "Group number must be between 1 and 18."
        return [
            atom
            for atom in self.__dict__.values()
            if isinstance(atom, Element) and atom.group == group_number
        ]

    def period(self, period_number: int) -> list[Element]:
        """Return all atoms in a period."""
        assert 1 <= period_number <= 7, "Period number must be between 1 and 7."
        return [
            atom
            for atom in self.__dict__.values()
            if isinstance(atom, Element) and atom.period == period_number
        ]

    def number(self, number: int) -> Element:
        """Return an atom by atomic number."""
        for atom in self.__dict__.values():
            if isinstance(atom, Element) and atom.number == number:
                return atom
        raise ValueError(f"No atom with atomic number {number}.")

    @property
    def sources(self) -> list[str]:
        """Return a list of sources for all elements."""
        sources = set()
        for atom in self.__dict__.values():
            if isinstance(atom, Element):
                sources.add(atom.mass.source)
                if atom.electronegativity:
                    sources.add(atom.electronegativity.source)
                if atom.atomic_radius:
                    sources.add(atom.atomic_radius.source)
                if atom.cov_radius:
                    sources.add(atom.cov_radius.source)
                if atom.vdw_radius:
                    sources.add(atom.vdw_radius.source)
                if atom.cov_radius_double:
                    sources.add(atom.cov_radius_double.source)
                if atom.cov_radius_triple:
                    sources.add(atom.cov_radius_triple.source)
        return list(sources)
    def show(self):
        """Print all atoms in a human-readable format."""
        print(f"Sources: {self.sources}\n")
        to_table([val for val in self.__dict__.values() if isinstance(val, Element)])


periodic_table = PeriodicTable.from_data()
"""Periodic table data from PubChem and other sources.

    Attributes:
        An attribute for each element in the periodic table, e.g. `periodic_table.H` for Hydrogen.
        Methods:
            group(group_number: int) -> list[Element]: Return all atoms in a group.
            period(period_number: int) -> list[Element]: Return all atoms in a period.
            number(number: int) -> Element: Return an atom by atomic number.
            show(): Print all atoms in a human-readable format.

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
