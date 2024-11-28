"""Math functions helpful for common CAD tasks."""


def evenly_space_with_center(
    center: float = 0,
    *,
    count: int,
    spacing: float,
) -> list[float]:
    """Evenly space `count` items around `center` with `spacing`."""
    half_spacing = (count - 1) * spacing / 2
    return [center - half_spacing + i * spacing for i in range(count)]
