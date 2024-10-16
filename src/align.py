"""Shortcut aliases for the Align class."""

import build123d as bd

TOP = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX)
BOTTOM = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
FRONT = (bd.Align.CENTER, bd.Align.MIN, bd.Align.CENTER)
BACK = (bd.Align.CENTER, bd.Align.MAX, bd.Align.CENTER)
CENTER = (bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER)
LEFT = (bd.Align.MIN, bd.Align.CENTER, bd.Align.CENTER)
RIGHT = (bd.Align.MAX, bd.Align.CENTER, bd.Align.CENTER)
