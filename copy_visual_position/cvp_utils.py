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

import bpy
import copy
import mathutils

def ApplyRealMatrixWorldObj(obj, matrix):
    for cons in obj.constraints:
        if cons.type == "CHILD_OF":
            if not cons.mute:
                if cons.target is not None:
                    Child = cons.inverse_matrix
                    par = cons.target.matrix_world
                    obj.matrix_world = Child.inverted() @ par.inverted() @ matrix
                    return
    obj.matrix_world = matrix


def ApplyRealMatrixWorldBones(bone, obj, matrix):
    for cons in bone.constraints:
        if cons.type == "CHILD_OF":
            if not cons.mute:
                if cons.target is not None:
                    Child = cons.inverse_matrix
                    if cons.target.type == "ARMATURE":
                        par = obj.matrix_world @ obj.pose.bones[cons.subtarget].matrix
                    else:
                        par = cons.target.matrix_world
                    bone.matrix = obj.matrix_world.inverted() @ (Child.inverted() @ par.inverted() @ matrix)
                    return
    bone.matrix = obj.matrix_world.inverted() @ matrix


def FindItemInListByName(item, list):
    for TargetItem in list:
        if TargetItem.name == item:
            return TargetItem
    return None

def SetVisualObjPos(obj, loc, rot, scale, UseLoc, UseRot, UseScale):
    # Save
    BaseLoc = copy.deepcopy(obj.location)
    BaseRot = copy.deepcopy(obj.rotation_euler)
    BaseScale = copy.deepcopy(obj.scale)
    # ApplyPos
    mat_loc = mathutils.Matrix.Translation(loc)
    mat_rot = rot.to_matrix().to_4x4()
    matrix = mat_loc @ mat_rot
    ApplyRealMatrixWorldObj(obj, matrix)
    obj.scale = scale
    # ResetNotDesiredValue
    if not UseLoc:
        obj.location = BaseLoc
    if not UseRot:
        obj.rotation_euler = BaseRot
    if not UseScale:
        obj.scale = BaseScale

def GetVisualVertLoc(obj):
    # Save
    BaseLoc = copy.deepcopy(bpy.context.scene.cursor.location)
    # ApplyPos
    bpy.ops.view3d.snap_cursor_to_selected()
    loc = copy.deepcopy(bpy.context.scene.cursor.location)
    bpy.context.scene.cursor.location = BaseLoc
    return(loc)


def SetVisualVertLoc(obj, loc):
    # Save
    BaseLoc = copy.deepcopy(bpy.context.scene.cursor.location)
    # ApplyPos
    bpy.context.scene.cursor.location = loc
    bpy.ops.view3d.snap_selected_to_cursor(use_offset=True)
    bpy.context.scene.cursor.location = BaseLoc


def GetVisualBonePos(obj, Bone):
    matrix_Pose = obj.matrix_world @ Bone.matrix
    loc = matrix_Pose @ mathutils.Vector((0, 0, 0))
    rot = matrix_Pose.to_euler()
    scale = Bone.scale
    return((loc, rot, scale))


def SetVisualBonePos(obj, Bone, loc, rot, scale, UseLoc, UseRot, UseScale):
    # Save
    BaseLoc = copy.deepcopy(Bone.location)
    BaseScale = copy.deepcopy(Bone.scale)
    RotModeBase = copy.deepcopy(Bone.rotation_mode)
    #Bone.rotation_mode = Bone.rotation_mode  # Need update for proxy
    BaseRot = copy.deepcopy(Bone.rotation_euler)
    # ApplyPos
    mat_loc = mathutils.Matrix.Translation(loc)
    mat_rot = rot.to_matrix().to_4x4()
    matrix = mat_loc @ mat_rot
    ApplyRealMatrixWorldBones(Bone, obj, matrix)
    Bone.scale = scale
    # ResetNotDesiredValue
    if not UseLoc:
        Bone.location = BaseLoc
    if not UseRot:
        Bone.rotation_euler = BaseRot
    if not UseScale:
        Bone.scale = BaseScale
    #Bone.rotation_mode = RotModeBase  # Need update for proxy

def GetVisualBonesPosPacked(obj, TargetBones):
    PositionList = []
    for bone in TargetBones:
        loc = GetVisualBonePos(obj, bone)[0]
        rot = GetVisualBonePos(obj, bone)[1]
        scale = GetVisualBonePos(obj, bone)[2]
        PositionList.append((bone.name, loc, rot, scale))
    return PositionList


def SetVisualBonesPosPacked(obj, TargetBones, PositionList, UseLoc, UseRot, UseScale):
    for pl in PositionList:
        TargetBone = FindItemInListByName(pl[0], TargetBones)
        if TargetBone is not None:
            loc = mathutils.Vector(pl[1])
            rot = mathutils.Euler(pl[2], 'XYZ')
            scale = mathutils.Vector(pl[3])
            SetVisualBonePos(obj, TargetBone, loc, rot, scale, UseLoc, UseRot, UseScale)
