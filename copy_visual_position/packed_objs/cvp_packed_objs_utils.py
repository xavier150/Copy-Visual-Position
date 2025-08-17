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

import mathutils
from .. import cvp_utils

def GetVisualObjsPosPacked(TargetObjs):
    PositionList = []
    for obj in TargetObjs:
        loc = obj.matrix_world @ (obj.location * 0)
        rot = obj.matrix_world.to_euler()
        scale = obj.scale
        PositionList.append((obj.name, loc, rot, scale))
    return PositionList


def SetVisualObjsPosPacked(TargetObjs, PositionList, UseLoc, UseRot, UseScale):
    for pl in PositionList:
        TargetBone = cvp_utils.FindItemInListByName(pl[0], TargetObjs)
        if TargetBone is not None:
            loc = mathutils.Vector(pl[1])
            rot = mathutils.Euler(pl[2], 'XYZ')
            scale = mathutils.Vector(pl[3])
            cvp_utils.SetVisualObjPos(TargetBone, loc, rot, scale, UseLoc, UseRot, UseScale)