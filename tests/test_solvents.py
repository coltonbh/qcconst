from qcconst import solvents


def test_solvents():
    # Assert that all solvents have a name, dielectric and sources
    for name in solvents.as_list():
        solvent = solvents[name]
        assert solvent.name
        assert solvent.dielectric
        assert isinstance(solvent.sources, list)
        assert solvent.sources


def test_show():
    solvents.show()
