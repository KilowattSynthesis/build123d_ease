"""Create a version of the `show()` function which runs silently in a CI environment."""

import os
from typing import TypeVar

import build123d as bd

T = TypeVar(
    "T",
    bd.BaseLineObject,
    bd.Curve,
    bd.Compound,
    bd.Part,
    bd.Face,
    bd.Edge,
    bd.Vertex,
    bd.Wire,
    bd.Solid,
    bd.Shape,
)


def _can_be_shown(obj: object) -> bool:
    """Return True if the object is show-able in the CAD viewer."""
    return isinstance(obj, T.__constraints__)


if os.getenv("CI"):

    def show(cad_obj: T, *args: object) -> T:  # type: ignore reportUnknownMemberType
        """Do nothing (dummy function) to skip showing the CAD model in CI."""
        if not _can_be_shown(cad_obj):
            msg = "The first argument must be a Part object."
            raise TypeError(msg)

        for obj in args:
            if not _can_be_shown(obj):
                msg = "The arguments must be Part, Face, Edge, or Vertex objects."
                raise TypeError(msg)

        return cad_obj
else:
    import ocp_vscode  # type: ignore reportMissingTypeStubs

    def show(cad_obj: T, *args: object) -> T:
        """Show the CAD model in the CAD viewer."""
        if not _can_be_shown(cad_obj):
            msg = "The first argument must be a Part object."
            raise TypeError(msg)

        ocp_vscode.show(cad_obj, *args)  # type: ignore reportUnknownMemberType
        return cad_obj
