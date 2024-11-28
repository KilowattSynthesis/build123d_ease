"""3D shapes, constructed with a BOSL2-like interface.

https://github.com/BelfrySCAD/BOSL2/wiki/shapes3d.scad
"""

import build123d as bd

from build123d_ease import faces


def rectangular_prism(
    size: float | tuple[float, float, float],
    *,
    anchor: faces.FaceSelectorType = None,
) -> bd.Part:
    """Create a rectangular prism.

    Args:
        size: The size of the prism.
        anchor: The face to anchor the prism to. If None, the prism is centered.

    Returns:
        The rectangular prism.

    """
    if isinstance(size, int | float):
        size = (size, size, size)

    x, y, z = size

    if anchor is None or anchor == "ALL":
        # Center the prism.
        return bd.Box(x, y, z)

    for axis_name, axis_value in zip("XYZ", anchor.to_tuple(), strict=True):
        if axis_value not in {-1, 0, 1}:
            msg = f"Invalid anchor value for axis '{axis_name}': {axis_value}"
            raise ValueError(msg)

    return bd.Box(x, y, z).translate(
        bd.Vector(-x / 2 * anchor.X, -y / 2 * anchor.Y, -z / 2 * anchor.Z)
    )
