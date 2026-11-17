---
name: skidl
description: Verified SKiDL 2.2.1 practices for Python schematics with KiCad libraries. Covers circuit scope, no-connect pins, an ERC gate that can fail, footprint checks and tests. Use when you write, change or review a SKiDL circuit.
---

# SKiDL

These facts are verified on SKiDL 2.2.1 with the KiCad 9 backend. For
another version, test the behaviour before you use it.

## Build a circuit

Build each circuit inside `with Circuit() as c:` and return `c`.

```python
from skidl import Circuit, Net, Part

def build():
    with Circuit() as c:
        vcc, gnd = Net("3V3"), Net("GND")
        r1 = Part("Device", "R", value="10k",
                  footprint="Resistor_SMD:R_0603_1608Metric", ref="R1")
        r1[1] += vcc
        r1[2] += gnd
    return c
```

- Pass `c` to each gate and each check.
- Do not call `skidl.ERC()`. It uses the first default circuit. Inside a
  `with Circuit()` block it checks an empty circuit and reports 0 errors.
  Call `c.ERC()`.
- Import the circuit module as a package. Do not edit `sys.path`.

## Unused pins

```python
for pin in ("2", "4", "6"):
    j1[pin] += c.NC
```

- Connect each unused pin to `c.NC`, the no-connect net of the circuit.
  SKiDL leaves these pins out of the netlist. This is correct for any
  number of pins.
- Do not make your own `NCNet` and put two or more pins on it. SKiDL 2.2.1
  writes it as an ordinary net, and the PCB then shorts the pins.

## ERC gate

Count the errors on `skidl.logger.erc_logger`. Do not read
`skidl.erc.active_logger` after ERC, because it always gives 0.

```python
from skidl.logger import erc_logger

def erc_error_count(c) -> int:
    c.ERC()
    return erc_logger.error.count

def assert_erc_clean(c) -> None:
    if not c.parts:
        raise AssertionError("the circuit has no parts")
    if erc_error_count(c):
        raise AssertionError("SKiDL ERC found errors")
```

- ERC resets the counters on each run.
- Refuse a circuit with no parts. Its ERC result is 0 and proves nothing.
- Warnings do not fail the gate. Read them and explain each one that stays.
- Keep a negative test that seeds a real conflict and proves that the gate
  fails:

```python
with Circuit() as bad:
    u1 = Part("74xx", "74LS04", ref="U1",
              footprint="Package_DIP:DIP-14_W7.62mm")
    clash = Net("CLASH")
    clash += u1[2], u1[4]          # two outputs on one net
    assert erc_error_count(bad) >= 1
```

## Footprints

- SKiDL 2.2.1 does not report an unknown footprint as an error.
- Resolve each `Library:Footprint` against KiCad's `fp-lib-table`. Make sure
  that `<library>/<name>.kicad_mod` exists.
- Keep a negative test with a footprint name that does not exist.
- Use only symbols and footprints that exist in the libraries. Do not
  invent names.

## Tests

- Assert each important net by its exact set of `(part.ref, pin.num)`.
- `tag=` is not the reference. A part with tag `R9` can get the reference
  `R3`. Use `ref` in each netlist assertion. Use tags only to find a part
  in memory.
- Assert that each unused pin satisfies `part[pin].net is c.NC`.
- Generate the netlist and assert the exact set of net names in it.
- The KiCad 9 netlist puts `(ref "J1")` and `(pin "2")` on separate lines.
  Thus a substring search for a node never finds a match, and can never
  fail. Match a node with a regex that accepts whitespace, for example
  `\(ref "J1"\)\s*\(pin "2"\)`, or parse the s-expression.
- For a board with only passive parts, ERC cannot find a wrong net on a
  pin. The pin-set assertions are the real check.

## Limits

- SKiDL 2.2.1 cannot write a `.kicad_sch` for KiCad 9 or 10. SKiDL ERC and
  the netlist are the schematic checks. Record this as a waiver.
- When a `.kicad_sch` or `.kicad_pcb` exists, run `kicad-cli` ERC or DRC with
  `--exit-code-violations`. Without this flag, the exit code is 0 when there
  are violations.

## BOM and part data

- Write the BOM with `csv.writer`.
- Do not write a part number (for example an LCSC number) or a rating
  without a source that you read. Leave the field blank and write
  "to verify".
