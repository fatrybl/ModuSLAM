# Open Issues

Open issues of https://github.com/fatrybl/ModuSLAM, exported on 2026-09-29 (8 issues).

## #14 Check incremental data batch creation.

- Opened by @fatrybl on 2024-04-30
- Labels: enhancement, update
- Assignees: @fatrybl
- Original: https://github.com/fatrybl/ModuSLAM/issues/14

Check if data batch can be created incrementally when a graph candidate has not been yet created but the batch has already been empty.

Will be solved after adding new sensor (except Lidar3D).

## #15 Use slots

- Opened by @fatrybl on 2024-05-01
- Labels: enhancement
- Assignees: @fatrybl
- Original: https://github.com/fatrybl/ModuSLAM/issues/15

Maybe start using __slots__ for some dataclasses ?

## #25 create full VO/VIO pipelines and feature map

- Opened by @fatrybl on 2024-07-29
- Labels: enhancement, update
- Assignees: @fatrybl
- Original: https://github.com/fatrybl/ModuSLAM/issues/25

1. Visual odometry with Smart Projection factors
2. Visual-Inertial odometry with Smart Projection factors + IMU
3. Trajectory map
4. Map with detected and triangulated features

## #27 Fix visual features pipeline with smart factors

- Opened by @fatrybl on 2024-09-18
- Labels: bug
- Original: https://github.com/fatrybl/ModuSLAM/issues/27

Now visual smart projection factors still do not work. It requires precise first approximation of poses. Otherwise the solution diverges.

## #28 Fix visual features mapping process

- Opened by @fatrybl on 2024-09-18
- Labels: bug
- Original: https://github.com/fatrybl/ModuSLAM/issues/28

Visual features map build process is not implemented

## #30 graphviz render problem.

- Opened by @fatrybl on 2024-10-23
- Last updated 2024-10-24
- Labels: bug
- Assignees: @Elzaaa
- Original: https://github.com/fatrybl/ModuSLAM/issues/30

Need to fix "source.render(dot)" in graph_saver.py  to be able to render pdf file properly

## #48 refactor imports

- Opened by @fatrybl on 2025-06-26
- Labels: bug, update
- Assignees: @fatrybl
- Original: https://github.com/fatrybl/ModuSLAM/issues/48

add required methods, classes, objects to __init__.py file of the corresponding modules to avoid long import promts.

## #51 refactor code to fit Python 3.12 standards

- Opened by @fatrybl on 2025-10-02
- Labels: wontfix, update
- Assignees: @fatrybl
- Original: https://github.com/fatrybl/ModuSLAM/issues/51

All code (especially custom type defs) should be refactored to fit the latest Python 3.12 standards.
