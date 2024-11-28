"""Vectors that refer to faces of a 3D object.

Based on BOSL2's orientation techniques:
https://github.com/BelfrySCAD/BOSL2/wiki/attachments.scad#subsection-orient
"""

from typing import Literal

import build123d as bd

TOP = UP = bd.Vector(0, 0, 1)
BOTTOM = BOT = DOWN = bd.Vector(0, 0, -1)
LEFT = bd.Vector(-1, 0, 0)
RIGHT = bd.Vector(1, 0, 0)
FRONT = FWD = FORWARD = bd.Vector(0, 1, 0)
BACK = bd.Vector(0, -1, 0)

FaceSelectorType = bd.Vector | Literal["ALL"] | None
EdgeSelectorType = bd.Vector | Literal["X", "Y", "Z", "ALL"] | None
CornerSelectorType = bd.Vector | Literal["ALL"] | None
