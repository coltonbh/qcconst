# QCConst

[![image](https://img.shields.io/pypi/v/qcconst.svg)](https://pypi.python.org/pypi/qcconst)
[![image](https://img.shields.io/pypi/l/qcconst.svg)](https://pypi.python.org/pypi/qcconst)
[![image](https://img.shields.io/pypi/pyversions/qcconst.svg)](https://pypi.python.org/pypi/qcconst)
[![Actions status](https://github.com/coltonbh/qcconst/workflows/Tests/badge.svg)](https://github.com/coltonbh/qcconst/actions)
[![Actions status](https://github.com/coltonbh/qcconst/workflows/Basic%20Code%20Quality/badge.svg)](https://github.com/coltonbh/qcconst/actions)

Physical constants, conversion factors, and a periodic table with clear source information for every value. Data from NIST CODATA 2022, Pubchem, and Washington University.

## Data Sources

Each piece of data contains a link to its source. Primary data sources include:
| Data Name | Source | Source Links |
| -------------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Physical Constants` | NIST 2022 CODATA | [Individual Constant Lookup](http://physics.nist.gov/constants), [Fundamenal Constants Listing](https://physics.nist.gov/cuu/Constants/Table/allascii.txt), [Conversion Factors](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8) |
| `Periodic Table` | PubChem | [Periodic Table](https://pubchem.ncbi.nlm.nih.gov/periodic-table/), [Raw CSV Data](https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV?response_type=save&response_basename=PubChemElements_all) |
| `Solvent Data` | University of Washington | [Solvent Properties](https://depts.washington.edu/eooptic/linkfiles/dielectric_chart%5B1%5D.pdf) |

## Installation

```sh
pip install qcconst
```

## Quickstart

### Constants

```python
>>> from qcconst import constants

>>> constants.BOHR_TO_ANGSTROM
0.529177210544, unit=Å, source=https://physics.nist.gov/cgi-bin/cuu/Value?bohrrada0

# Use constants just like a float
>>> constants.BOHR_TO_ANGSTROM * 10
5.29177210544

# Know the source of every constant
>>> constants.BOHR_TO_ANGSTROM.source
'https://physics.nist.gov/cgi-bin/cuu/Value?bohrrada0'

# See sources for all constants
>>> constants.sources
['https://physics.nist.gov/cgi-bin/cuu/Value?bohrrada0', 'https://physics.nist.gov/cgi-bin/cuu/Value?hrj|search_for=hartree+to+joule', 'https://physics.nist.gov/cuu/Constants/Table/allascii.txt', 'https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8']

# List all available constants
>>> constants.as_list()
['ANGSTROM_TO_BOHR', 'AVOGADRO_NUMBER', 'BOHR_TO_ANGSTROM', 'BOLTZMANN_CONSTANT', 'HARTREE_TO_JOULE', 'HARTREE_TO_KCAL_PER_MOL', 'KCAL_TO_JOULE', ...]

# Human readable print out of all available constants
>>> constants.show()
name                              value  unit      source
-----------------------  --------------  --------  ---------------------------------------------------------
ANGSTROM_TO_BOHR            1.88973      Bohr      Derived as 1 / BOHR_TO_ANGSTROM
AVOGADRO_NUMBER             6.02214e+23  mol⁻¹     https://physics.nist.gov/cuu/Constants/Table/allascii.txt
BOHR_TO_ANGSTROM            0.529177     Å         https://physics.nist.gov/cgi-bin/cuu/Value?bohrrada0
BOLTZMANN_CONSTANT          1.38065e-23  J/K       https://physics.nist.gov/cuu/Constants/Table/allascii.txt
...
```

### Periodic Table

```python
>>> from qcconst import periodic_table as pt

>>> pt.Ni
Atom(symbol='Ni', number=28, name='Nickel', mass=58.6934, group=10, period=4, block='d', electron_config='[Ar] 3d8 4s2')

>>>pt.Ni.number
28

>>> pt.group(1)
[Atom(symbol='H', number=1, name='Hydrogen', mass=1.00784, group=1, period=1, block='s', electron_config='1s1'),
Atom(symbol='Li', number=3, name='Lithium', mass=6.94, group=1, period=2, block='s', electron_config='[He] 2s1'),
Atom(symbol='Na', number=11, name='Sodium', mass=22.98976928, group=1, period=3, block='s', electron_config='[Ne] 3s1'),
Atom(symbol='K', number=19, name='Potassium', mass=39.0983, group=1, period=4, block='s', electron_config='[Ar] 4s1'),
Atom(symbol='Rb', number=37, name='Rubidium', mass=85.4678, group=1, period=5, block='s', electron_config='[Kr] 5s1'),
Atom(symbol='Cs', number=55, name='Cesium', mass=132.90545196, group=1, period=6, block='s', electron_config='[Xe] 6s1'),
Atom(symbol='Fr', number=87, name='Francium', mass=223.0, group=1, period=7, block='s', electron_config='[Rn] 7s1')]

>>> pt.period(3)
[Atom(symbol='Na', number=11, name='Sodium', mass=22.9897693, group=1, period=3, block='Alkali metal', electron_config='[Ne]3s1'),
Atom(symbol='Mg', number=12, name='Magnesium', mass=24.305, group=2, period=3, block='Alkaline earth metal', electron_config='[Ne]3s2'),
Atom(symbol='Al', number=13, name='Aluminum', mass=26.981538, group=13, period=3, block='Post-transition metal', electron_config='[Ne]3s2 3p1'),
Atom(symbol='Si', number=14, name='Silicon', mass=28.085, group=14, period=3, block='Metalloid', electron_config='[Ne]3s2 3p2'),
Atom(symbol='P', number=15, name='Phosphorus', mass=30.973762, group=15, period=3, block='Nonmetal', electron_config='[Ne]3s2 3p3'),
Atom(symbol='S', number=16, name='Sulfur', mass=32.07, group=16, period=3, block='Nonmetal', electron_config='[Ne]3s2 3p4'),
Atom(symbol='Cl', number=17, name='Chlorine', mass=35.45, group=17, period=3, block='Halogen', electron_config='[Ne]3s2 3p5'),
Atom(symbol='Ar', number=18, name='Argon', mass=39.9, group=18, period=3, block='Noble gas', electron_config='[Ne]3s2 3p6')]

# Know the sources of the data
>>> pt.sources
['https://pubchem.ncbi.nlm.nih.gov/periodic-table']

# Human readable print out of the Periodic Table data
>>> pt.show()
Sources: https://pubchem.ncbi.nlm.nih.gov/periodic-table, https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV?response_type=save&response_basename=PubChemElements_all

symbol      number  name                mass    group    period  block                  electron_config
--------  --------  -------------  ---------  -------  --------  ---------------------  ---------------------------------
H                1  Hydrogen         1.008          1         1  Nonmetal               1s1
He               2  Helium           4.0026        18         1  Noble gas              1s2
Li               3  Lithium          7              1         2  Alkali metal           [He]2s1
Be               4  Beryllium        9.01218        2         2  Alkaline earth metal   [He]2s2
B                5  Boron           10.81          13         2  Metalloid              [He]2s2 2p1
C                6  Carbon          12.011         14         2  Nonmetal               [He]2s2 2p2
N                7  Nitrogen        14.007         15         2  Nonmetal               [He] 2s2 2p3
...
```

### Solvents

Solvents are accessed with a dictionary lookup rather than attribute lookup because many of their names are invalid Python attributes (i.e., they start with a number or contain `-` characters). For example, `solvents.1,2-dimethoxyethane` is invalid syntax. As a result, solvents are looked up using `solvents['name']` rather than `solvents.name`.

```python
from qcconst import solvents

>>> solvents["1,4-dioxane"]
Solvent(name='1,4-dioxane', dielectric=2.25, sources=['https://depts.washington.edu/eooptic/linkfiles/dielectric_chart%5B1%5D.pdf'])

>>> solvents["1,4-dioxane"].dielectric
2.25

# Will return None if solvent not found
>>> solvents.get("Fake Solvent")
>>>

# List all available solvents
>>> solvents.as_list()
['acetic acid', 'acetone', 'acetonitrile', 'anisole', 'benzene', 'bromobenzene', 'carbon disulfide', 'carbon tetrachloride', 'chlorobenzene', 'chloroform', 'cyclohexane', 'dibutyl ether', 'o-dichlorobenzene', '1,2-dichloroethane', 'dichloromethane', 'diethylamine', 'diethyl ether', '1,2-dimethoxyethane', 'n', 'n,n-dimethylformamide', 'dimethyl sulfoxide', '1,4-dioxane', 'ethanol', 'ethyl acetate', 'ethyl benzoate', 'formamide', 'hexamethylphosphoramide', 'isopropyl alcohol', 'methanol', '2-methyl-2-propanol', 'nitrobenzene', 'nitromethane', 'pyridine', 'tetrahydrofuran', 'toluene', 'trichloroethylene', 'triethylamine', 'trifluoroacetic acid', '2,2,2-trifluoroethanol', 'water', 'o-xylene', ...]

# Know the sources of the data
>>> solvents["water"].sources
['https://depts.washington.edu/eooptic/linkfiles/dielectric_chart%5B1%5D.pdf']

# Human readable print out of all available solvents
>>> solvents.show()
name                       dielectric  sources
-----------------------  ------------  ------------------------------------------------------------------------------
acetic acid                      6.15  ['https://depts.washington.edu/eooptic/linkfiles/dielectric_chart%5B1%5D.pdf']
acetone                         20.7   ['https://depts.washington.edu/eooptic/linkfiles/dielectric_chart%5B1%5D.pdf']
acetonitrile                    37.5   ['https://depts.washington.edu/eooptic/linkfiles/dielectric_chart%5B1%5D.pdf']
anisole                          4.33  ['https://depts.washington.edu/eooptic/linkfiles/dielectric_chart%5B1%5D.pdf']
benzene                          2.27  ['https://depts.washington.edu/eooptic/linkfiles/dielectric_chart%5B1%5D.pdf']
bromobenzene                     5.17  ['https://depts.washington.edu/eooptic/linkfiles/dielectric_chart%5B1%5D.pdf']
...
```

## Adding New Values

Adding new values is simple! Just add it to one of the `.csv` files in [src/qcconst/data](https://github.com/coltonbh/qcconst/tree/master/src/qcconst/data). Include the value, its source, and any other required metadata and then open a PR. That's it! ✨

## The QC Suite of Programs

If you like `qcconst` you may like my other libraries for computational chemistry.

- [qcio](https://github.com/coltonbh/qcio) - Elegant and intuitive data structures for quantum chemistry, featuring seamless Jupyter Notebook visualizations. [Documentation](https://qcio.coltonhicks.com)
- [qcparse](https://github.com/coltonbh/qcparse) - A library for efficient parsing of quantum chemistry data into structured `qcio` objects.
- [qcop](https://github.com/coltonbh/qcop) - A package for operating quantum chemistry programs using `qcio` standardized data structures. Compatible with `TeraChem`, `psi4`, `QChem`, `NWChem`, `ORCA`, `Molpro`, `geomeTRIC` and many more.
- [BigChem](https://github.com/mtzgroup/bigchem) - A distributed application for running quantum chemistry calculations at scale across clusters of computers or the cloud. Bring multi-node scaling to your favorite quantum chemistry program.
- `ChemCloud` - A [web application](https://github.com/mtzgroup/chemcloud-server) and associated [Python client](https://github.com/mtzgroup/chemcloud-client) for exposing a BigChem cluster securely over the internet.
