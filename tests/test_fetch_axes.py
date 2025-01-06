"""Tests for the `fetch axes` module."""

from math import sqrt

import build123d as bd

import build123d_ease as bde


def test_axis_from_cylindrical_face() -> None:
    """Validates if an axis for a simple cylinder could be found."""
    p = bd.Part(None) + bd.Cylinder(
        radius=10,
        height=10,
    )
    face = p.faces().filter_by(bd.GeomType.CYLINDER)[0]
    calculated_axis = bde.axis_from_cylindrical_face(face)
    expected_axis = bd.Axis((0, 0, 0), (0, 0, 1))

    assert expected_axis == calculated_axis


def test_axis_from_cylindrical_face_diagonal_pin() -> None:
    """Validate behavior when a pin is not aligned with an axis."""
    p = bd.Part(None) + bd.Cylinder(
        radius=10,
        height=10,
    ).rotate(axis=bd.Axis.X, angle=45)
    face = p.faces().filter_by(bd.GeomType.CYLINDER)[0]

    result_axis = bde.axis_from_cylindrical_face(face)

    expected_axis = bd.Axis((0, 0, 0), (0, -sqrt(2) / 2, sqrt(2) / 2))
    assert expected_axis == result_axis
