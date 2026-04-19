"""Example of a rounded box."""

import build123d as bd

import build123d_ease as bde
from build123d_ease import show


def part1() -> bd.Part | bd.Compound:
    """Create a CAD model of part1."""
    p = bd.Part(None)

    # All edges
    p += bd.Pos(X=0) * bde.RoundedBox(10, 8, 6, radius=1, edges="ALL")

    # Only Z-parallel edges
    p += bd.Pos(X=12) * bde.RoundedBox(10, 8, 6, radius=1, edges="Z")

    # Top face edges only (face pointing toward +Z)
    p += bd.Pos(X=24) * bde.RoundedBox(10, 8, 6, radius=1, edges=(0, 0, 1))

    # All except bottom face
    p += bd.Pos(X=36) * bde.RoundedBox(
        10, 8, 6, radius=1, edges="ALL", except_edges=(0, 0, -1)
    )

    return p


if __name__ == "__main__":
    parts = {
        "part1": show(part1()),
    }
