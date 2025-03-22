from dataclasses import fields, is_dataclass
from typing import Optional

from tabulate import tabulate


def to_table(objects, headers: Optional[list[str]] = None):
    """Convert a list of dataclass objects into a nicely formatted table."""
    if not objects:
        print("No data to display.")
        return

    first_obj = objects[0]

    if isinstance(first_obj, dict):
        headers = headers or list(first_obj.keys())
        rows = [[obj.get(h, "") for h in headers] for obj in objects]
    elif is_dataclass(first_obj):
        headers = headers or [field.name for field in fields(first_obj)]
        rows = [[getattr(obj, h, "") for h in headers] for obj in objects]
    else:  # Regular Python objects
        headers = headers or list(vars(first_obj).keys())
        rows = [[getattr(obj, h, "") for h in headers] for obj in objects]

    print(tabulate(rows, headers=headers))
