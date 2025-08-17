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

from . import cvp_packed_bones_props
from . import cvp_packed_bones_ui
from . import cvp_packed_bones_utils

import importlib
if "cvp_packed_bones_props" in locals():
    importlib.reload(cvp_packed_bones_props)
if "cvp_packed_bones_ui" in locals():
    importlib.reload(cvp_packed_bones_ui)
if "cvp_packed_bones_utils" in locals():
    importlib.reload(cvp_packed_bones_utils)



# ############################[...]#############################


classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    cvp_packed_bones_props.register()
    cvp_packed_bones_ui.register()
    


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    cvp_packed_bones_ui.unregister()
    cvp_packed_bones_props.unregister()