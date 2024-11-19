# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================

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