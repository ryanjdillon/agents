---
name: build123d
description: Verified build123d 0.11.1 practices to build, measure, test and export parametric CAD parts in Python. Use when you write, change or review a build123d part or its tests.
---

# build123d

These facts are verified on build123d 0.11.1. For another version, or for
an API that is not here, test it in a short script before you use it.

## Parameters

- Put the dimensions in a `dataclass`. Give each dimension a name. Calculate
  derived sizes from the named dimensions.
- Check each range in `__post_init__`. Raise `ValueError` with the limit and
  the value.
- Write one test for each invalid value. The test makes sure that the
  constructor raises `ValueError`.

```python
@dataclass
class RingParams:
    inner_radius: float = 67.5
    wall: float = 3.0
    height: float = 41.0

    def __post_init__(self) -> None:
        if self.wall <= 0:
            raise ValueError(f"wall ({self.wall}) must be > 0")
```

## Build

```python
from build123d import Align, Cylinder, Pos, Rotation

ring = Cylinder(70, 50) - Cylinder(65, 50)  # centred: z -25..25
boss = Cylinder(20, 30, rotation=(0, 90, 0), align=Align.CENTER).moved(Pos(70, 0, 0))
bore = Pos(70, 0, 0) * Rotation(0, 90, 0) * Cylinder(16, 40)
part = (ring + boss) - bore  # add material first, then cut
assert len(part.solids()) == 1 and part.is_valid
```

- Primitives are centred on the origin unless you give `align=`.
- `Rotation(x, y, z)` takes degrees. Do not use `math.degrees()` or
  `math.radians()` on the angle.
- Add all material first, then cut all holes. If you cut before you add,
  the added material fills the hole again.
- A bore through a curved wall leaves crescent lips of wall if its flat end
  starts on the wall surface. Start the bore inside the cavity.

## Measure

There is no `Shape.section()` method in 0.11.1. To get a cross-section, use
the algebra-mode operation `section()`. It returns a `Sketch`.

```python
from build123d import Box, GeomType, Plane, Pos, section

cut = section(part, Plane.XY, height=0)  # the Sketch at z = 0
print(cut.area)

bb = part.bounding_box()
print(bb.min, bb.max, bb.size)
print(part.volume)
for e in part.edges().filter_by(GeomType.CIRCLE):
    print(round(e.radius, 3), e.arc_center)


def overlap_volume(part, probe) -> float:
    """intersect returns a ShapeList, or None when nothing meets."""
    found = part.intersect(probe)
    return sum(s.volume for s in found) if found else 0.0


print(overlap_volume(part, Pos(x, y, z) * Box(1, 1, 1)))
```

- Compare the volume with a hand estimate. Accept about 10 % difference.
- Probe for material where it must be and where it must not be.
- At a bore through a curved wall, probe just inside the bore outline, at
  the wall. A probe at the bore axis does not find lips.
- If a probe shows a circular edge that you did not expect, find its cause.
  Treat it as a defect until you can explain it.

## Test

- Build the part and compare the model with the parameters. Measure the
  bounding box, radii, positions and volume.
- Do not compare a parameter with a parameter.
- Assert the envelope on all three axes, for the default and each variant.
  Material outside the envelope is a defect.
- For each variant, assert the dimension that the variant changes.
- Import the part as a package (`from mypackage.part import build`). Do not edit
  `sys.path`.

## Export

```python
from build123d import export_step, export_stl

export_step(part, "build/part.step")  # raises RuntimeError on failure
if not export_stl(part, "build/part.stl"):
    raise RuntimeError("STL export failed")
```

- `export_step` raises `RuntimeError` when the write fails. Do not catch
  it to continue.
- `export_stl` returns `False` when it fails. Check the result.
- Remove old files before you export, so that a failed export does not
  leave a stale file.
- After the export, make sure that each file exists and is not empty.
- Write exports to a build directory, not to the repo.

## Self-check

1. The part is one valid solid.
2. The bounding box agrees with the envelope on all three axes.
3. The volume is within about 10 % of a hand estimate.
4. Each important feature is measured from the solid.
5. Each variant that the tests use passes items 1 to 4.
