"""
Select the NGC 628 PHANGS fields overlapping the requested imaging footprint.

Run this with a Python environment containing casatools and casatasks:

    python run_field_selection_pipeline_phangs-alma.py

Each selected measurement set is written beside its input with the suffix
".split.fields". This script is self-contained and does not import the PHANGS
pipeline or analysisUtils.
"""

import os
import shutil

import numpy as np
from casatasks import split
from casatools import msmetadata, table


ms_root = "/nfs/home/abarnes/PHANGS/ALMA/uvdata/"

relative_ms_paths = [
    # 7-m data
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57d/calibrated/uid___A002_X6f1341_X80b.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57d/calibrated/uid___A002_X6f2c6e_Xb0a.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57d/calibrated/uid___A002_X7fc9da_X1f0d.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57d/calibrated/uid___A002_X7fc9da_X4b45.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57d/calibrated/uid___A002_X8081ba_X11fb.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57d/calibrated/uid___A002_X8081ba_X3e04.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57d/calibrated/uid___A002_X8081ba_X44b8.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57d/calibrated/uid___A002_X8081ba_X85e.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57d/calibrated/uid___A002_X8081ba_Xce1.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57d/calibrated/uid___A002_X8204db_X4f.ms.split.cal",
    # 12-m data
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57b/calibrated/uid___A002_X5b2f01_X3f.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57b/calibrated/uid___A002_X8081ba_X4018.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57b/calibrated/uid___A002_X8081ba_X4527.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57b/calibrated/uid___A002_X80c782_X1911.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57b/calibrated/uid___A002_X8204db_X611.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57b/calibrated/uid___A002_X95b353_X471.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57b/calibrated/uid___A002_X960614_X2d5b.ms.split.cal",
    "2012.1.00650.S/science_goal.uid___A002_X5a9a13_X579/group.uid___A002_X5a9a13_X57a/member.uid___A002_X5a9a13_X57b/calibrated/uid___A002_X966cea_X96c.ms.split.cal",
]

ms_list = [os.path.join(ms_root, path) for path in relative_ms_paths]

lower_left = ("01:36:46.3246735920", "+15:45:57.1071148991")
upper_right = ("01:36:42.5660666166", "+15:46:48.5652118062")
output_suffix = ".split.fields"
overwrite = False


def hms_to_degrees(value):
    hours, minutes, seconds = (float(part) for part in value.split(":"))
    return 15.0 * (hours + minutes / 60.0 + seconds / 3600.0)


def dms_to_degrees(value):
    sign = -1.0 if value.startswith("-") else 1.0
    degrees, minutes, seconds = (
        float(part) for part in value.lstrip("+-").split(":")
    )
    return sign * (degrees + minutes / 60.0 + seconds / 3600.0)


def get_selected_fields(vis):
    tb = table()
    tb.open(os.path.join(vis, "FIELD"))
    field_ids = np.arange(tb.nrows())
    directions = tb.getcol("DELAY_DIR")
    tb.close()

    field_ra = np.rad2deg(directions[0, 0, :]) % 360.0
    field_dec = np.rad2deg(directions[1, 0, :])

    tb.open(os.path.join(vis, "ANTENNA"))
    antenna_diameter = float(np.mean(tb.getcol("DISH_DIAMETER")))
    tb.close()

    msmd = msmetadata()
    msmd.open(vis)
    science_spws = msmd.spwsforintent("OBSERVE_TARGET#ON_SOURCE")
    minimum_frequency = min(
        float(np.min(msmd.chanfreqs(int(spw)))) for spw in science_spws
    )
    msmd.close()

    # Match the PHANGS utility default: retain fields within 0.8 primary-beam
    # FWHM of the requested rectangle.
    pb_fwhm_arcsec = (
        1.14
        * 1.22
        * (299792458.0 / minimum_frequency)
        * 206264.806
        / antenna_diameter
    )
    match_radius_arcsec = 0.8 * pb_fwhm_arcsec

    ra1, dec1 = hms_to_degrees(lower_left[0]), dms_to_degrees(lower_left[1])
    ra2, dec2 = hms_to_degrees(upper_right[0]), dms_to_degrees(upper_right[1])
    minimum_ra, maximum_ra = sorted((ra1, ra2))
    minimum_dec, maximum_dec = sorted((dec1, dec2))

    minimum_ra -= match_radius_arcsec / 3600.0 / np.cos(np.deg2rad(minimum_dec))
    maximum_ra += match_radius_arcsec / 3600.0 / np.cos(np.deg2rad(maximum_dec))
    minimum_dec -= match_radius_arcsec / 3600.0
    maximum_dec += match_radius_arcsec / 3600.0

    keep = (
        (field_ra >= minimum_ra)
        & (field_ra <= maximum_ra)
        & (field_dec >= minimum_dec)
        & (field_dec <= maximum_dec)
    )
    return [str(field_id) for field_id in field_ids[keep]], pb_fwhm_arcsec


for index, vis in enumerate(ms_list, start=1):
    if not os.path.isdir(vis):
        print("Missing input, skipping: {}".format(vis))
        continue

    outputvis = vis + output_suffix
    if os.path.exists(outputvis):
        if not overwrite:
            print("Existing output, skipping: {}".format(outputvis))
            continue
        backup = outputvis + ".backup"
        if os.path.exists(backup):
            shutil.rmtree(backup)
        shutil.move(outputvis, backup)

    selected_fields, pb_fwhm = get_selected_fields(vis)
    if not selected_fields:
        print("No overlapping fields in: {}".format(vis))
        continue

    tb = table()
    tb.open(vis)
    datacolumn = "corrected" if "CORRECTED_DATA" in tb.colnames() else "data"
    tb.close()

    field_selection = ",".join(selected_fields)
    print(
        "[{}/{}] Selecting {} fields (PB FWHM {:.1f} arcsec) from {}".format(
            index, len(ms_list), len(selected_fields), pb_fwhm, vis
        )
    )
    split(
        vis=vis,
        outputvis=outputvis,
        field=field_selection,
        datacolumn=datacolumn,
    )
    print("Wrote: {}".format(outputvis))
