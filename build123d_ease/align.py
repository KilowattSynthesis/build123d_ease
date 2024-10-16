"""Shortcut aliases for the Align class.

The names specify the "anchor" point. For example, "BOTTOM" means to align the bottom of
the object to the origin.
"""

import build123d as bd

TOP = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX)
BOTTOM = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
FRONT = (bd.Align.CENTER, bd.Align.MIN, bd.Align.CENTER)
BACK = (bd.Align.CENTER, bd.Align.MAX, bd.Align.CENTER)
LEFT = (bd.Align.MIN, bd.Align.CENTER, bd.Align.CENTER)
RIGHT = (bd.Align.MAX, bd.Align.CENTER, bd.Align.CENTER)

CENTER = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER)

TOP_LEFT = (bd.Align.MIN, bd.Align.MIN, bd.Align.MAX)
TOP_RIGHT = (bd.Align.MAX, bd.Align.MIN, bd.Align.MAX)
BOTTOM_LEFT = (bd.Align.MIN, bd.Align.MAX, bd.Align.MAX)
BOTTOM_RIGHT = (bd.Align.MAX, bd.Align.MAX, bd.Align.MAX)

FRONT_LEFT = (bd.Align.MIN, bd.Align.MIN, bd.Align.CENTER)
FRONT_RIGHT = (bd.Align.MAX, bd.Align.MIN, bd.Align.CENTER)
BACK_LEFT = (bd.Align.MIN, bd.Align.MAX, bd.Align.CENTER)
BACK_RIGHT = (bd.Align.MAX, bd.Align.MAX, bd.Align.CENTER)
