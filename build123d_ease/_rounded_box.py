"""RoundedBox - a BOSL2-style rounded box for build123d.

Edge Specification
------------------
The `edges` and `except_edges` parameters accept any of:

  * "ALL"   - all 12 edges
  * "NONE"  - no edges
  * "X"     - the 4 edges parallel to the X axis
  * "Y"     - the 4 edges parallel to the Y axis
  * "Z"     - the 4 edges parallel to the Z axis
  * A 3-tuple / Vector pointing toward a **face**   → all 4 edges of that face
  * A 3-tuple / Vector pointing toward an **edge**  → that single edge
  * A 3-tuple / Vector pointing toward a **corner** → the 3 edges touching that corner
  * A list of any of the above, which are unioned together.

`except_edges` uses the same descriptors and is subtracted from `edges`.
"""

from typing import Literal

import build123d as bd

# ---------------------------------------------------------------------------
# Internal edge table
# ---------------------------------------------------------------------------
# We number the 12 edges 0-11 in BOSL2 order:
#   0- 3 : X-parallel  (vary in Y and Z)
#   4- 7 : Y-parallel  (vary in X and Z)
#   8-11 : Z-parallel  (vary in X and Y)
#
# Each entry stores (axis, sign_a, sign_b) where axis is the direction the
# edge runs and sign_a, sign_b are the signs of the two *fixed* coordinates.
#
# Layout mirrors BOSL2:
#   row 0  [Y-Z-, Y+Z-, Y-Z+, Y+Z+]   X-parallel, fixed (y,z)
#   row 1  [X-Z-, X+Z-, X-Z+, X+Z+]   Y-parallel, fixed (x,z)
#   row 2  [X-Y-, X+Y-, X-Y+, X+Y+]   Z-parallel, fixed (x,y)

_EDGE_TABLE = [
    # Each index: (run_axis, fixed_axis_1, sign_1, fixed_axis_2, sign_2)
    # --- X-parallel (row 0) ---
    (0, 1, -1, 2, -1),  #  0: Y- Z-
    (0, 1, +1, 2, -1),  #  1: Y+ Z-
    (0, 1, -1, 2, +1),  #  2: Y- Z+
    (0, 1, +1, 2, +1),  #  3: Y+ Z+
    # --- Y-parallel (row 1) ---
    (1, 0, -1, 2, -1),  #  4: X- Z-
    (1, 0, +1, 2, -1),  #  5: X+ Z-
    (1, 0, -1, 2, +1),  #  6: X- Z+
    (1, 0, +1, 2, +1),  #  7: X+ Z+
    # --- Z-parallel (row 2) ---
    (2, 0, -1, 1, -1),  #  8: X- Y-
    (2, 0, +1, 1, -1),  #  9: X+ Y-
    (2, 0, -1, 1, +1),  # 10: X- Y+
    (2, 0, +1, 1, +1),  # 11: X+ Y+
]

# Pre-built named masks
_ALL_MASK = [True] * 12
_NONE_MASK = [False] * 12


def _axis_mask(axis: int) -> list[bool]:
    """Edges running along the given axis (0=X, 1=Y, 2=Z)."""
    return [e[0] == axis for e in _EDGE_TABLE]


# ---------------------------------------------------------------------------
# Descriptor → mask
# ---------------------------------------------------------------------------

EdgeDescriptor = (
    Literal["ALL", "NONE", "X", "Y", "Z"]
    | list[str]
    | tuple[float, float, float]
    | list[list[int]]
)


def _vec_to_mask(v: tuple[float, float, float]) -> list[bool]:  # noqa: C901
    """Interpret a 3-vector as a face / edge / corner selector.

    Return a 12-element boolean mask.
    """

    # Normalise to a list of ints in {-1, 0, +1}
    def _sign(x: float) -> int:
        if x > 0.5:  # noqa: PLR2004
            return 1
        if x < -0.5:  # noqa: PLR2004
            return -1
        return 0

    sx, sy, sz = _sign(v[0]), _sign(v[1]), _sign(v[2])
    non_zero = sum(c != 0 for c in (sx, sy, sz))

    mask = [False] * 12
    for i, (run, fa, sa, fb, sb) in enumerate(_EDGE_TABLE):
        # Map axis indices to sign values from the vector
        signs = [sx, sy, sz]
        fixed_sign_a = signs[fa]
        fixed_sign_b = signs[fb]

        if non_zero == 0:
            # zero vector → nothing
            pass
        elif non_zero == 1:
            # Points toward a face: select all 4 edges of that face.
            # The face normal axis has a non-zero sign; the edge must be
            # fixed at that sign on that axis.
            if (
                (sx != 0 and run != 0 and fa == 0 and sa == sx)
                or (sx != 0 and run != 0 and fb == 0 and sb == sx)
                or (sy != 0 and run != 1 and fa == 1 and sa == sy)
                or (sy != 0 and run != 1 and fb == 1 and sb == sy)
                or (sz != 0 and run != 2 and fa == 2 and sa == sz)  # noqa: PLR2004
                or (sz != 0 and run != 2 and fb == 2 and sb == sz)  # noqa: PLR2004
            ):
                mask[i] = True
        elif non_zero == 2:  # noqa: PLR2004
            # Points toward an edge: the edge's two fixed coordinates must
            # match the two non-zero signs of the vector.
            if fixed_sign_a == signs[fa] and fixed_sign_b == signs[fb]:  # noqa: SIM102
                # Both fixed coords must be constrained AND match
                if (
                    signs[fa] != 0
                    and signs[fb] != 0
                    and fixed_sign_a == signs[fa]
                    and fixed_sign_b == signs[fb]
                ):
                    mask[i] = True
        # non_zero == 3: points toward a corner.
        # Select edges that touch this corner, i.e. edges whose two
        # fixed-axis signs both match the vector.
        elif fixed_sign_a == signs[fa] and fixed_sign_b == signs[fb]:
            mask[i] = True

    return mask


def _descriptor_to_mask(descriptor: EdgeDescriptor) -> list[bool]:
    """Convert a single edge set descriptor to a 12-element boolean mask."""
    if isinstance(descriptor, str):
        s = descriptor.upper()
        if s == "ALL":
            return list(_ALL_MASK)
        if s == "NONE":
            return list(_NONE_MASK)
        if s == "X":
            return _axis_mask(0)
        if s == "Y":
            return _axis_mask(1)
        if s == "Z":
            return _axis_mask(2)
        msg = f"Unknown edge string descriptor: {descriptor!r}"
        raise ValueError(msg)

    # Otherwise treat as a 3-vector.
    arr = list(descriptor)
    if len(arr) == 3 and not hasattr(arr[0], "__len__"):  # noqa: PLR2004
        return _vec_to_mask(arr)  # pyright: ignore[reportArgumentType]

    msg_0 = f"Unrecognised edge descriptor: {descriptor!r}"
    raise ValueError(msg_0)


def _resolve_edges(
    edges: EdgeDescriptor | list[EdgeDescriptor],
    except_edges: EdgeDescriptor | list[EdgeDescriptor] | None = None,
) -> list[bool]:
    """Combine `edges` and `except_edges` into a single 12-element boolean mask."""

    def _union(descriptors: EdgeDescriptor | list[EdgeDescriptor]) -> list[bool]:
        # Wrap a bare descriptor in a list
        if isinstance(descriptors, str) or (
            hasattr(descriptors, "__len__")
            and len(descriptors) == 3  # noqa: PLR2004
            and not hasattr(descriptors[0], "__len__")
        ):
            descriptors = [descriptors]  # pyright: ignore[reportAssignmentType]
        mask = list(_NONE_MASK)
        for d in descriptors:
            dm = _descriptor_to_mask(d)  # pyright: ignore[reportArgumentType]
            mask = [a or b for a, b in zip(mask, dm, strict=True)]
        return mask

    include = _union(edges)

    if except_edges is not None:
        exclude = _union(except_edges)
        include = [a and not b for a, b in zip(include, exclude, strict=True)]

    return include


# ---------------------------------------------------------------------------
# build123d edge matching
# ---------------------------------------------------------------------------


def _midpoint(edge: bd.Edge) -> tuple[float, float, float]:
    """Return the midpoint of a build123d Edge."""
    # Use the bounding-box centre along the edge curve
    bb = edge.bounding_box()
    return (
        (bb.min.X + bb.max.X) / 2,
        (bb.min.Y + bb.max.Y) / 2,
        (bb.min.Z + bb.max.Z) / 2,
    )


def _classify_edge(
    edge: bd.Edge, tol: float = 1e-6
) -> tuple[int, float, float, float] | None:
    """Return (run_axis, fixed_sign_a, fixed_sign_b, fa, fb) for a box edge.

    That is, return which _EDGE_TABLE row it matches.  Returns None for diagonal/curved.
    """
    bb = edge.bounding_box()
    dx = abs(bb.max.X - bb.min.X)
    dy = abs(bb.max.Y - bb.min.Y)
    dz = abs(bb.max.Z - bb.min.Z)

    if dx > tol and dy <= tol and dz <= tol:
        run = 0
    elif dy > tol and dx <= tol and dz <= tol:
        run = 1
    elif dz > tol and dx <= tol and dy <= tol:
        run = 2
    else:
        return None  # diagonal or curved

    mx, my, mz = _midpoint(edge)
    return run, mx, my, mz


def _match_edge_index(edge: bd.Edge, half: tuple[float, float, float]) -> int | None:
    """Return the index (0-11) in _EDGE_TABLE that this edge corresponds to, or None.

    Argument: the half-dimensions (hx, hy, hz) of the box.
    """
    info = _classify_edge(edge)
    if info is None:
        return None

    run, mx, my, mz = info
    hx, hy, hz = half

    def _s(val: float, h: float) -> int:
        if val > h * 0.5:
            return 1
        if val < -h * 0.5:
            return -1
        return 0

    coords = [_s(mx, hx), _s(my, hy), _s(mz, hz)]

    for i, (r, fa, sa, fb, sb) in enumerate(_EDGE_TABLE):
        if r != run:
            continue
        if coords[fa] == sa and coords[fb] == sb:
            return i

    return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def RoundedBox(  # noqa: N802, PLR0913
    length: float,
    width: float,
    height: float,
    rotation: bd.RotationLike = (0, 0, 0),
    align: bd.Align | tuple[bd.Align, bd.Align, bd.Align] = (
        bd.Align.CENTER,
        bd.Align.CENTER,
        bd.Align.CENTER,
    ),
    *,
    radius: float,
    edges: EdgeDescriptor | list[EdgeDescriptor] = "ALL",
    except_edges: EdgeDescriptor | list[EdgeDescriptor] | None = None,
) -> bd.Part:
    """Create a rectangular box with selectively rounded edges.

    Parameters
    ----------
    length : float
        Dimension along the X axis.
    width : float
        Dimension along the Y axis.
    height : float
        Dimension along the Z axis.
    rotation
        angles to rotate about axes. Defaults to (0, 0, 0).
    align :
        align min, center,
        or max of object. Defaults to (Align.CENTER, Align.CENTER, Align.CENTER).
    radius : float
        Fillet radius applied to selected edges.
    edges : edge descriptor or list thereof
        Edges to round.  Defaults to ``"ALL"``.
    except_edges : edge descriptor or list thereof, optional
        Edges to exclude from rounding.

    Returns
    -------
    bd.Part

    """
    mask = _resolve_edges(edges, except_edges)

    # Build the box
    with bd.BuildPart() as bp:
        bd.Box(length, width, height, rotation=rotation, align=align)

    part = bp.part
    if part is None:
        msg = "Unexpectedly failed to build box"
        raise RuntimeError(msg)

    # Nothing to round - return a plain box
    if not any(mask):
        return part

    half = (length / 2, width / 2, height / 2)

    # Gather edges that match the mask
    selected: list[bd.Edge] = []
    for edge in part.edges():  # pyright: ignore[reportOptionalMemberAccess]
        idx = _match_edge_index(edge, half)
        if idx is not None and mask[idx]:
            selected.append(edge)

    if not selected:
        return part

    # Apply fillet.
    return part.fillet(radius, selected)
