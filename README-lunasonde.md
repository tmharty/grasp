# Lunasonde fork of GRaSP

This is a fork of [porpass/grasp](https://github.com/porpass/grasp) kept by
Lunasonde so that `lunasonde-core` can depend on GRaSP's signal-processing
core (`grasp.processing`, `grasp.postprocessing`, `grasp.datuming`) without
installing the planetary-mission stack (SPICE, PDS readers, DEM/CRS, SEG-Y).

## What differs from upstream

The `light` branch carries exactly three changes on top of upstream `main`:

| File | Change |
| --- | --- |
| `pyproject.toml` | core `dependencies` are numpy + scipy; everything else moved to a new `planetary` extra; `test` depends on `grasp[planetary]` |
| `src/grasp/__init__.py` | public names resolve lazily (PEP 562 `__getattr__`) from a `_LAZY` map that mirrors `__all__` |
| `src/grasp/common/utils.py` | `pvl` and `pds4_tools` are imported inside `parse_pds_lbl` / `parse_pds_xml` |

Plus `tests/unit/test_light_imports.py`, which proves the core imports only
numpy and scipy, and this file. Nothing under `src/grasp/processing/`,
`postprocessing/`, `datuming/` or `simulation/` is modified.

Install the core: `pip install git+https://github.com/tmharty/grasp@<tag>`.
Install everything upstream needs: `pip install "grasp[planetary] @ git+https://github.com/tmharty/grasp@<tag>"`.

## Tags

Fork tags are `v<upstream version>-lunasonde.<n>`, e.g. `v0.6.0a3-lunasonde.1`.
`lunasonde-core` pins one of these; never pin the branch.

## Syncing with upstream

Upstream follows Git Flow; track its `main` releases, not `develop`.

```bash
git remote add upstream https://github.com/porpass/grasp.git   # once
git fetch upstream --tags
git checkout light
git merge upstream/main
```

Expected conflicts, and only these:

- `src/grasp/__init__.py`: upstream added or removed an export. Keep the
  lazy form and add/remove the matching `_LAZY` entry so that
  `test_all_public_names_are_lazily_mapped` passes.
- `pyproject.toml`: upstream bumped a pin or added a dependency. Keep
  numpy/scipy in `dependencies` and put anything new under `planetary`.
- `src/grasp/common/utils.py`: only if upstream touched the two parse
  functions or the import block.

Then verify and tag:

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[test]"
pytest tests/unit
git tag v<upstream version>-lunasonde.1 && git push origin light --tags
```

Finally bump the `grasp @ git+https://...` pin in `lunasonde-core/pyproject.toml`
and run its `tests/processing` parity tests.

## Offering the change upstream

The import-hygiene change is small and BSD-3 licensed. If upstream adopts
it (a `planetary` extra plus lazy `__init__`), this fork can become a plain
mirror and `lunasonde-core` can pin upstream tags directly.
