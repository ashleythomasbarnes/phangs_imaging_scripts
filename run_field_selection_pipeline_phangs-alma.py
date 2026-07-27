"""
Select the NGC 628 PHANGS fields overlapping the requested imaging footprint.

Run this script inside CASA from the phangs_imaging_scripts repository root.
Each selected measurement set is written beside its input with the suffix
".split.fields".
"""

import os

from phangsPipeline import utilsFieldSelection


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

utilsFieldSelection.process_ms_list(
    ms_list=ms_list,
    lower_left_ra_dec="J2000 01:36:46.3246735920 +15:45:57.1071148991",
    upper_right_ra_dec="J2000 01:36:42.5660666166 +15:46:48.5652118062",
    suffix=".split.fields",
    overwrite=False,
    verbose=True,
)
