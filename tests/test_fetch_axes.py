"""Tests for the `fetch axes` module."""

import build123d as bd

import build123d_ease as bde


def test_axis_from_cylindric_faces() -> None:
    """Validates if an axis for a simple cylinder could be found."""
    p = bd.Part(None) + bd.Cylinder(
        radius=10,
        height=10,
    )
    face = p.faces().filter_by(bd.GeomType.CYLINDER)[0]
    calculated_axis = bde.axis_from_cylindric_faces(face)
    expected_axis = bd.Axis((0, 0, 0), (0, 0, 1))

    assert expected_axis == calculated_axis
