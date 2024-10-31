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
