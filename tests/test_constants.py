from qcconst import constants


def test_constants():
    # Assert that all constants have a unit and source
    for name in constants.as_list():
        constant = getattr(constants, name)
        assert constant  # Not None
        assert constant.unit
        assert constant.source


def test_sources():
    assert isinstance(constants.sources, list)


def test_show():
    constants.show()


def test_repr():
    constant = constants.HARTREE_TO_KCAL_PER_MOL
    assert isinstance(repr(constant), str)
