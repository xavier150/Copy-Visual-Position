# SPDX-FileCopyrightText: 2018-2025 Xavier Loux (BleuRaven)
#
# SPDX-License-Identifier: GPL-3.0-or-later

# ----------------------------------------------
#  Copy Visual Position
#  https://github.com/xavier150/Copy-Visual-Position
# ----------------------------------------------

# ----------------------------------------------
#  with this Addons you will be able to easily copy and paste the visual position of an object in your scene, this works also for Vertices in EditMode and also the chains of Bones in PoseMode
#  xavierloux.com
# ----------------------------------------------


import bpy





classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.LastVisualLocation = bpy.props.FloatVectorProperty(
        name="VisualLocation",
        description="",
        default=(0, 0, 0),
        precision=40,
        size=3
        )

    bpy.types.Scene.LastVisualRotation = bpy.props.FloatVectorProperty(
        name="VisualRotation",
        description="",
        default=(0, 0, 0),
        precision=40,
        size=3
        )

    bpy.types.Scene.LastVisualScale = bpy.props.FloatVectorProperty(
        name="VisualScale:",
        description="",
        default=(1, 1, 1),
        precision=40,
        size=3
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.LastVisualScale
    del bpy.types.Scene.LastVisualRotation
    del bpy.types.Scene.LastVisualLocation