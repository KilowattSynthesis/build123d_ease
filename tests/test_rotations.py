"""Tests for the `rotation` module."""

# pyright: reportCallIssue=information

import build123d as bd

import build123d_ease as bde


def test_pos_x_rotation() -> None:
    """Applying the POS_X rotation to a cylinder will make it point that direction."""
    p = bd.Part() + bd.Cylinder(
        radius=10,
        height=10,
        rotation=bde.rotation.POS_X,
        align=bde.align.BOTTOM,  # Align bottom happens **before** the rotation.
    )

    part_pos_x = p & bd.Box(100, 100, 100, align=bde.align.LEFT)
    assert p.volume == part_pos_x.volume


def test_neg_x_rotation() -> None:
    """Applying the NEG_X rotation to a cylinder will make it point that direction."""
    p = bd.Part() + bd.Cylinder(
        radius=10,
        height=10,
        rotation=bde.rotation.NEG_X,
        align=bde.align.BOTTOM,  # Align bottom happens **before** the rotation.
    )

    part_neg_x = p & bd.Box(100, 100, 100, align=bde.align.RIGHT)
    assert p.volume == part_neg_x.volume


def test_pos_y_rotation() -> None:
    """Applying the POS_Y rotation to a cylinder will make it point that direction."""
    p = bd.Part() + bd.Cylinder(
        radius=10,
        height=10,
        rotation=bde.rotation.POS_Y,
        align=bde.align.BOTTOM,  # Align bottom happens **before** the rotation.
    )

    part_pos_y = p & bd.Box(100, 100, 100, align=bde.align.FRONT)
    assert p.volume == part_pos_y.volume


def test_neg_y_rotation() -> None:
    """Applying the NEG_Y rotation to a cylinder will make it point that direction."""
    p = bd.Part() + bd.Cylinder(
        radius=10,
        height=10,
        rotation=bde.rotation.NEG_Y,
        align=bde.align.BOTTOM,  # Align bottom happens **before** the rotation.
    )

    part_neg_y = p & bd.Box(100, 100, 100, align=bde.align.BACK)
    assert p.volume == part_neg_y.volume


# We will just trust that POS_Z (no rotation) and NEG_Z (a 180-degree rotation) work as
# expected, without tests.
