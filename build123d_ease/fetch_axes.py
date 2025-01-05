"""Fetch axes from a build123d Face objects."""

import build123d as bd


def axis_from_cylindric_faces(face: bd.Face) -> bd.Axis:
    """Return a the central axis for a cylindrical face.

    Returns:
        bd.Axis: The central axis through the cyindrical face.

    """
    position = 0.5 * (face.position_at(0, 0.5) + face.position_at(0.5, 0.5))
    direction = next(
        edge.location_at(1).to_axis().direction
        for edge in face.edges()
        if not edge.is_closed
    )
    return bd.Axis(position, direction)
