from typing import Optional


class Value(float):
    """A float subclass holding additional metadata.

    Uncertainty should be set to 0.0 for exact values, None if not applicable or no
    data is available.
    """

    unit: str
    source: str
    uncertainty: Optional[float]
    notes: str

    def __new__(
        cls, value, unit: str, source: str, uncertainty: Optional[float], notes: str
    ):
        obj = float.__new__(cls, value)
        obj.unit = unit
        obj.source = source
        obj.uncertainty = uncertainty
        obj.notes = notes
        return obj

    def __repr__(self):
        return f"{float(self)}, unit={self.unit}, uncertainty={self.uncertainty} source={self.source} {'notes=' + self.notes if self.notes else ''}"
