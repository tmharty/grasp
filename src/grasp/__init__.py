# SPDX-License-Identifier: BSD-3-Clause
from importlib.metadata import metadata, version
from email.utils import parseaddr

# TODO Audit __init__
__version__ = version("grasp")
_meta = metadata("grasp")
__author__ = parseaddr(_meta["Author-email"])[0]
__description__ = _meta["Summary"]
__license__ = _meta["License-Expression"]

# Custom fields with no PEP 621 home — keep as literals
__funding__ = "NASA Planetary Data Archival, Restoration, and Tools (PDART)"
__grants__ = "80NSSC20K1057"

###########################################################################
#
# Public API
#
# Every public name is resolved lazily (PEP 562) so that importing the
# signal-processing core -- grasp.processing, grasp.postprocessing,
# grasp.datuming -- pulls in only numpy and scipy. Names that need the
# ``planetary`` extra (SPICE, PDS readers, DEM/CRS, SEG-Y, plotting) are
# imported the first time they are accessed, e.g. ``grasp.radar_sounder``.
#
# Keep ``_LAZY`` in sync with ``__all__`` below.
#
###########################################################################
_LAZY: dict[str, tuple[str, str]] = {
    # Common
    "determine_observation_years": ("grasp.common", "determine_observation_years"),
    # Input
    "check_supported": ("grasp.input", "check_supported"),
    "grab_radar_params": ("grasp.input", "grab_radar_params"),
    "identify_file": ("grasp.input", "identify_file"),
    "load": ("grasp.input", "load"),
    "load_job": ("grasp.input", "load_job"),
    "read": ("grasp.input", "read"),
    # Processing (numpy/scipy only)
    "adaptive_spectral_notch": ("grasp.processing", "adaptive_spectral_notch"),
    "broadening_factor": ("grasp.processing", "broadening_factor"),
    "create_complex_baseband_chirp": ("grasp.processing", "create_complex_baseband_chirp"),
    "create_filter": ("grasp.processing", "create_filter"),
    "create_sharad_calibrated_chirp": ("grasp.processing", "create_sharad_calibrated_chirp"),
    "form_window": ("grasp.processing", "form_window"),
    "form_window_bandlimited": ("grasp.processing", "form_window_bandlimited"),
    "ionosphere_campbell": ("grasp.processing", "ionosphere_campbell"),
    "ionospheric_compensation": ("grasp.processing", "ionospheric_compensation"),
    "ionosphere_contrast": ("grasp.processing", "ionosphere_contrast"),
    "range_compress": ("grasp.processing", "range_compress"),
    "suppress_emi": ("grasp.processing", "suppress_emi"),
    "threshold_emi": ("grasp.processing", "threshold_emi"),
    "to_complex_baseband": ("grasp.processing", "to_complex_baseband"),
    # The radar_sounder class
    "radar_sounder": ("grasp.instantiator", "radar_sounder"),
    # The Processor
    "print_job_summary": ("grasp.grasp", "print_job_summary"),
    "process": ("grasp.grasp", "process_job"),
    # SPICE routines
    "compute_geodetic_position": ("grasp.spice", "compute_geodetic_position"),
    "compute_geometry": ("grasp.spice", "compute_geometry"),
    "compute_sza": ("grasp.spice", "compute_sza"),
    "compute_state_vectors": ("grasp.spice", "compute_state_vectors"),
    "decompose_velocity": ("grasp.spice", "decompose_velocity"),
    "et2utc": ("grasp.spice", "et2utc"),
    "find_mk_files": ("grasp.spice", "find_mk_files"),
    "furnish": ("grasp.spice", "furnish"),
    "get_radii": ("grasp.spice", "get_radii"),
    "grab_spice_params": ("grasp.spice", "grab_spice_params"),
    "print_mk_paths": ("grasp.spice", "print_mk_paths"),
    "unload": ("grasp.spice", "unload"),
    "utc2et": ("grasp.spice", "utc2et"),
    # Geospatial routines
    "extract_dem_swath": ("grasp.geospatial.extract_dem_swath", "extract_dem_swath"),
    "mars_lle_crs": ("grasp.geospatial.crs", "MARS_LLE"),
    "moon_lle_crs": ("grasp.geospatial.crs", "MOON_LLE"),
    "phobos_lle_crs": ("grasp.geospatial.crs", "PHOBOS_LLE"),
    "gcs_2000_crs": ("grasp.geospatial.crs", "gcs_2000_crs"),
    "geocent_crs": ("grasp.geospatial.crs", "geocent_crs"),
    # Azimuth processing (numpy/scipy only)
    "unfocused": ("grasp.processing.sar.unfocused", "unfocused"),
    "backscatter": ("grasp.processing.sar.range_doppler", "backscatter"),
    "range_doppler": ("grasp.processing.sar.range_doppler", "range_doppler"),
    "determine_aperture_bounds": ("grasp.processing.sar.utils", "determine_aperture_bounds"),
    "determine_output_frames": ("grasp.processing.sar.utils", "determine_output_frames"),
    "determine_aperture_resolution": ("grasp.processing.sar.utils", "determine_aperture_resolution"),
    "determine_aperture_step": ("grasp.processing.sar.utils", "determine_aperture_step"),
    "max_unaliased_aperture": ("grasp.processing.sar.utils", "max_unaliased_aperture"),
    "check_aperture": ("grasp.processing.sar.utils", "check_aperture"),
    "multilook": ("grasp.postprocessing.multilook", "multilook"),
    # Output
    "to_image": ("grasp.output.images", "to_image"),
    "radargram_with_dem": ("grasp.output.images", "radargram_with_dem"),
    "plot_dem_swath": ("grasp.output.plotting", "plot_dem_swath"),
    "write_grasp_output": ("grasp.output.writers", "write_grasp_output"),
    "export_segy": ("grasp.output.writers", "export_segy"),
    # Simulation
    "simulate_clutter": ("grasp.simulation.clutter", "simulate_clutter"),
}


def __getattr__(name: str):
    """Resolve a public name on first access (PEP 562)."""
    try:
        module_name, attr = _LAZY[name]
    except KeyError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None
    from importlib import import_module

    value = getattr(import_module(module_name), attr)
    globals()[name] = value  # cache so __getattr__ runs once per name
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(_LAZY))


__all__ = [
    ###################################################################################################################
    #
    # METADATA
    #
    ###################################################################################################################
    "__author__",
    "__license__",
    "__version__",
    "__description__",
    "__funding__",
    "__grants__",
    ###################################################################################################################
    #
    # Common Functions
    #
    ###################################################################################################################
    "determine_observation_years",
    ###################################################################################################################
    #
    # Input Functions
    #
    ###################################################################################################################
    "check_supported",
    "grab_radar_params",
    "identify_file",
    "load",
    "load_job",
    "read",
    ###################################################################################################################
    #
    # Classes
    #
    ###################################################################################################################
    "radar_sounder",
    ###################################################################################################################
    #
    # Processor
    #
    ###################################################################################################################
    "process",
    "print_job_summary",
    ###################################################################################################################
    #
    # SPICE Functions
    #
    ###################################################################################################################
    "compute_geodetic_position",
    "compute_geometry",
    "compute_state_vectors",
    "compute_sza",
    "decompose_velocity",
    "et2utc",
    "find_mk_files",
    "furnish",
    "get_radii",
    "grab_spice_params",
    "print_mk_paths",
    "unload",
    "utc2et",
    ###################################################################################################################
    #
    # Geospatial Functions
    #
    ###################################################################################################################
    "extract_dem_swath",
    "mars_lle_crs",
    "moon_lle_crs",
    "phobos_lle_crs",
    ###################################################################################################################
    #
    # Window Functions
    #
    ###################################################################################################################
    "form_window",
    "form_window_bandlimited",
    "create_complex_baseband_chirp",
    "to_complex_baseband",
    ###################################################################################################################
    #
    # Range Processing Functions
    #
    ###################################################################################################################
    "range_compress",
    ###################################################################################################################
    #
    # EMI Functions
    #
    ###################################################################################################################
    "adaptive_spectral_notch",
    "suppress_emi",
    "threshold_emi",
    ###################################################################################################################
    #
    # Ionospheric Correction Functions
    #
    ###################################################################################################################
    "ionosphere_campbell",
    "ionospheric_compensation",
    "ionosphere_contrast",
    ###################################################################################################################
    #
    # Common Azimuth Processing Functions
    #
    ###################################################################################################################
    "determine_aperture_resolution",
    "determine_aperture_step",
    "determine_aperture_bounds",
    "max_unaliased_aperture",
    "check_aperture",
    ###################################################################################################################
    #
    # Azimuth Processing
    #
    ###################################################################################################################
    "unfocused",
    "backscatter",
    "multilook",
    "simulate_clutter",
    ###################################################################################################################
    #
    # Plotting Functions
    #
    ###################################################################################################################
    "plot_dem_swath",
    ###################################################################################################################
    #
    # Output Functions
    #
    ###################################################################################################################
    # Output Functions
    "radargram_with_dem",
    "to_image",
    "write_grasp_output",
    "export_segy",
]