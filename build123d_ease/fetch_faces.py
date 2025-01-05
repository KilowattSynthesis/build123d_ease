"""Fetch faces by name from a build123d Part object."""

from typing import Literal

import build123d as bd


def top_face_of(part: bd.Part) -> bd.Face:
    """Return the top face of the given Part object."""
    return part.faces().sort_by(bd.Axis.Z)[-1]


def bottom_face_of(part: bd.Part) -> bd.Face:
    """Return the bottom face of the given Part object."""
    return part.faces().sort_by(bd.Axis.Z)[0]


def left_face_of(part: bd.Part) -> bd.Face:
    """Return the left face of the given Part object."""
    return part.faces().sort_by(bd.Axis.X)[0]


def right_face_of(part: bd.Part) -> bd.Face:
    """Return the right face of the given Part object."""
    return part.faces().sort_by(bd.Axis.X)[-1]


def front_face_of(part: bd.Part) -> bd.Face:
    """Return the front face of the given Part object."""
    return part.faces().sort_by(bd.Axis.Y)[0]


def back_face_of(part: bd.Part) -> bd.Face:
    """Return the back face of the given Part object."""
    return part.faces().sort_by(bd.Axis.Y)[-1]


def cylindric_faces(
    part: bd.Part, cylinder_type: Literal["hole", "pin"] | None = None
) -> list[bd.Face]:
    """Return a list of cylindric faces of the given Part object.

    Returns:
        list[bd.Face]: a list of requested face.

    """

    def is_valid_candidate(face: bd.Face) -> bool:
        center_position = 0.5 * (face.position_at(0, 0.5) + face.position_at(0.5, 0.5))
        is_inside = part.is_inside(center_position)

        if cylinder_type == "hole":
            return not is_inside
        if cylinder_type == "pin":
            return is_inside
        return True

    faces = part.faces().filter_by(bd.GeomType.CYLINDER)
    valid_faces = (
        face
        for face in faces
        if any(edge.is_closed for edge in face.edges())  # Only full cylinders.
    )

    filtered_faces = filter(is_valid_candidate, valid_faces)

    return list(filtered_faces)


def get_face_by_name(
    part: bd.Part,
    face_name: Literal["top", "bottom", "left", "right", "front", "back"],
) -> bd.Face:
    """Return the face of the given Part object with the given name.

    Raises:
        ValueError: If the face name is invalid.

    Returns:
        bd.Face: The requested face.

    """
    if face_name == "top":
        return top_face_of(part)
    if face_name == "bottom":
        return bottom_face_of(part)
    if face_name == "left":
        return left_face_of(part)
    if face_name == "right":
        return right_face_of(part)
    if face_name == "front":
        return front_face_of(part)
    if face_name == "back":
        return back_face_of(part)

    msg = f"Invalid face name: {face_name}"
    raise ValueError(msg)
