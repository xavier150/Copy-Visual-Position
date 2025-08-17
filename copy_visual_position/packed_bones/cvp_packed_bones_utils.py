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

def GetVisualBonesPosPacked(obj, TargetBones):
    PositionList = []
    for bone in TargetBones:
        loc = cvp_utils.GetVisualBonePos(obj, bone)[0]
        rot = cvp_utils.GetVisualBonePos(obj, bone)[1]
        scale = cvp_utils.GetVisualBonePos(obj, bone)[2]
        PositionList.append((bone.name, loc, rot, scale))
    return PositionList


def SetVisualBonesPosPacked(obj, TargetBones, PositionList, UseLoc, UseRot, UseScale):
    for pl in PositionList:
        TargetBone = cvp_utils.FindItemInListByName(pl[0], TargetBones)
        if TargetBone is not None:
            loc = mathutils.Vector(pl[1])
            rot = mathutils.Euler(pl[2], 'XYZ')
            scale = mathutils.Vector(pl[3])
            cvp_utils.SetVisualBonePos(obj, TargetBone, loc, rot, scale, UseLoc, UseRot, UseScale)