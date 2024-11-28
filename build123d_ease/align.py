"""Shortcut aliases for the Align class.

The names specify the "anchor" point. For example, "ANCHOR_BOTTOM" means to align the
bottom of the object to the origin.
"""

import build123d as bd

ANCHOR_TOP = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX)
ANCHOR_BOTTOM = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
ANCHOR_FRONT = (bd.Align.CENTER, bd.Align.MIN, bd.Align.CENTER)
ANCHOR_BACK = (bd.Align.CENTER, bd.Align.MAX, bd.Align.CENTER)
ANCHOR_LEFT = (bd.Align.MIN, bd.Align.CENTER, bd.Align.CENTER)
ANCHOR_RIGHT = (bd.Align.MAX, bd.Align.CENTER, bd.Align.CENTER)

ANCHOR_CENTER = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER)

ANCHOR_TOP_LEFT = (bd.Align.MIN, bd.Align.MIN, bd.Align.MAX)
ANCHOR_TOP_RIGHT = (bd.Align.MAX, bd.Align.MIN, bd.Align.MAX)
ANCHOR_BOTTOM_LEFT = (bd.Align.MIN, bd.Align.MAX, bd.Align.MAX)
ANCHOR_BOTTOM_RIGHT = (bd.Align.MAX, bd.Align.MAX, bd.Align.MAX)

ANCHOR_FRONT_LEFT = (bd.Align.MIN, bd.Align.MIN, bd.Align.CENTER)
ANCHOR_FRONT_RIGHT = (bd.Align.MAX, bd.Align.MIN, bd.Align.CENTER)
ANCHOR_BACK_LEFT = (bd.Align.MIN, bd.Align.MAX, bd.Align.CENTER)
ANCHOR_BACK_RIGHT = (bd.Align.MAX, bd.Align.MAX, bd.Align.CENTER)
