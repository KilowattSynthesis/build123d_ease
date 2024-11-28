"""Extensions, tools, and shortcuts to make modelling with Build123d easier."""

from . import align, fetch_faces, rotation
from .ci_show import show
from .fetch_faces import (
    back_face_of,
    bottom_face_of,
    front_face_of,
    left_face_of,
    right_face_of,
    top_face_of,
)
from .math import evenly_space_with_center

__VERSION__ = "0.1.2.2"

__all__ = [
    "align",
    "rotation",
    "show",
    "fetch_faces",
    "top_face_of",
    "bottom_face_of",
    "left_face_of",
    "right_face_of",
    "front_face_of",
    "back_face_of",
    "evenly_space_with_center",
]
