# SPDX-License-Identifier: BSD-3-Clause
"""The signal-processing core imports only numpy and scipy.

``grasp.processing``, ``grasp.postprocessing`` and ``grasp.datuming`` are
usable without the ``planetary`` extra. Each check runs in a subprocess
because the rest of the test session has long since imported the heavy
modules.
"""
import subprocess
import sys

import pytest

PLANETARY_ROOTS = (
    "spiceypy", "rasterio", "geopandas", "pyproj", "segyio", "h5py",
    "pvl", "pds4_tools", "matplotlib", "pandas", "shapely", "bitstring",
)

CORE_IMPORTS = (
    "import grasp",
    "import grasp.processing",
    "import grasp.postprocessing",
    "import grasp.datuming",
    "import grasp.processing.sar.dispatch",
    "from grasp import range_compress, suppress_emi, unfocused, "
    "range_doppler, backscatter, multilook, form_window, create_filter",
)


def _loaded_roots(statement: str) -> set[str]:
    script = (
        f"import sys; {statement}; "
        "print(','.join(sorted({m.split('.')[0] for m in sys.modules})))"
    )
    proc = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True, text=True, check=True,
    )
    return set(proc.stdout.strip().split(","))


@pytest.mark.parametrize("statement", CORE_IMPORTS)
def test_core_imports_pull_in_no_planetary_dependency(statement):
    roots = _loaded_roots(statement)
    leaked = roots & set(PLANETARY_ROOTS)
    assert not leaked, f"{statement!r} imported {sorted(leaked)}"


def test_all_public_names_are_lazily_mapped():
    import grasp

    public = {n for n in grasp.__all__ if not n.startswith("__")}
    missing = public - set(grasp._LAZY)
    assert not missing, f"__all__ names without a _LAZY entry: {sorted(missing)}"
    assert set(grasp._LAZY) <= set(dir(grasp))


def test_unknown_attribute_raises_attribute_error():
    import grasp

    with pytest.raises(AttributeError):
        grasp.definitely_not_a_grasp_name
