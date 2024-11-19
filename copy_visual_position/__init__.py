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
import bmesh
import mathutils
import math
import copy
from math import radians
from mathutils import *
from bpy.props import (
        StringProperty,
        FloatProperty,
        IntProperty,
        FloatVectorProperty,
        CollectionProperty,
        )


bl_info = {
    'name': 'Copy Visual Position',
    'description': "This addons Copy Visual Position allows to easily copy / paste the visual position of several elements in the scene like Objects, Bones or Vertex and other element in EditMod.",
    'author': 'Loux Xavier (BleuRaven)',
    'version': (0, 1, 5),
    'blender': (2, 90, 0),
    'location': 'View3D > UI > Copy Visual Position',
    'warning': '',
    "wiki_url": "https://github.com/xavier150/Copy-Visual-Position",
    'tracker_url': '',
    'support': 'COMMUNITY',
    'category': '3D_interaction'}


# ########################## [UI (One by one)] ###########################


class CVP_PT_VisualPoseOneByOne(bpy.types.Panel):  # Is Export panel
    bpy.types.Scene.LastVisualLocation = FloatVectorProperty(
        name="VisualLocation",
        description="",
        default=(0, 0, 0),
        precision=40,
        size=3
        )

    bpy.types.Scene.LastVisualRotation = FloatVectorProperty(
        name="VisualRotation",
        description="",
        default=(0, 0, 0),
        precision=40,
        size=3
        )

    bpy.types.Scene.LastVisualScale = FloatVectorProperty(
        name="VisualScale:",
        description="",
        default=(1, 1, 1),
        precision=40,
        size=3
        )

    bl_idname = "CVP_PT_VisualPoseOneByOne"
    bl_label = "One by one"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Copy visual position"

    def draw(self, context):
        scn = context.scene
        prop = bpy.types.Scene
        layout = self.layout
        value = layout
        value.prop(scn, 'LastVisualLocation')
        value.prop(scn, 'LastVisualRotation')
        value.prop(scn, 'LastVisualScale')

        text = layout.row()
        text.label(text="Copy visual position from active", icon='COPYDOWN')
        text.label(text="Paste visual position to active", icon='PASTEDOWN')
        Buttons = layout.row(align=True).column()
        Button_loc = Buttons.row()
        Button_rot = Buttons.row()
        Button_scale = Buttons.row()
        Button_all = Buttons.row()

        Button_loc.operator("object.copy_visual_location", icon='ORIENTATION_VIEW')
        Button_rot.operator("object.copy_visual_rotation", icon='ORIENTATION_LOCAL')
        Button_scale.operator("object.copy_scale", icon='ORIENTATION_NORMAL')
        Button_all.operator("object.copy_visual_all", icon='URL')

        Button_loc.operator("object.paste_visual_location", icon='ORIENTATION_VIEW')
        Button_rot.operator("object.paste_visual_rotation", icon='ORIENTATION_LOCAL')
        Button_scale.operator("object.paste_scale", icon='ORIENTATION_NORMAL')
        Button_all.operator("object.paste_visual_all", icon='URL')

        if bpy.context.active_object is None:
            Buttons.enabled = False
        if bpy.context.object is not None:
            if bpy.context.object.mode == "EDIT":
                Button_rot.enabled = False
                Button_scale.enabled = False
                Button_all.enabled = False
        else:
            Button_rot.enabled = False
            Button_scale.enabled = False
            Button_all.enabled = False

# ########################## [Buttons (One by one) ] ###########################


class CVP_OT_CopyVisualObjLocButton(bpy.types.Operator):
    bl_label = "Copy loc"
    bl_idname = "object.copy_visual_location"
    bl_description = "Contpy the visual location of the active object"

    def execute(self, context):
        scene = bpy.context.scene
        obj = bpy.context.active_object
        if bpy.context.object.mode == "OBJECT":
            scene.LastVisualLocation = obj.matrix_world @ (obj.location * 0)
        if bpy.context.object.mode == "POSE":
            scene.LastVisualLocation = GetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone)[0]
        if bpy.context.object.mode == "EDIT":
            scene.LastVisualLocation = GetVisualVertLoc(bpy.context.active_object)
        return {'FINISHED'}


class CVP_OT_CopyVisualObjRotButton(bpy.types.Operator):
    bl_label = "Copy rot"
    bl_idname = "object.copy_visual_rotation"
    bl_description = "Copy the visual rotation of the active object"

    def execute(self, context):
        scene = bpy.context.scene
        obj = bpy.context.active_object
        if bpy.context.object.mode == "OBJECT":
            scene.LastVisualRotation = obj.matrix_world.to_euler()
        if bpy.context.object.mode == "POSE":
            scene.LastVisualRotation = GetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone)[1]
        return {'FINISHED'}


class CVP_OT_CopyObjScaleButton(bpy.types.Operator):
    bl_label = "Copy scale"
    bl_idname = "object.copy_scale"
    bl_description = "Copy the scale of the active object"

    def execute(self, context):
        scene = bpy.context.scene
        obj = bpy.context.active_object
        if bpy.context.object.mode == "OBJECT":
            scene.LastVisualScale = obj.scale
        if bpy.context.object.mode == "POSE":
            scene.LastVisualScale = GetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone)[2]
        return {'FINISHED'}


class CVP_OT_CopyVisualObjPosButton(bpy.types.Operator):
    bl_label = "Copy all"
    bl_idname = "object.copy_visual_all"
    bl_description = "Copy the visual position of the active object"

    def execute(self, context):
        scene = bpy.context.scene
        obj = bpy.context.active_object
        if bpy.context.object.mode == "OBJECT":
            scene.LastVisualLocation = obj.matrix_world @ (obj.location * 0)
            scene.LastVisualRotation = obj.matrix_world.to_euler()
            scene.LastVisualScale = obj.scale
        if bpy.context.object.mode == "POSE":
            Trans = GetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone)
            scene.LastVisualLocation = Trans[0]
            scene.LastVisualRotation = Trans[1]
            scene.LastVisualScale = Trans[2]
        return {'FINISHED'}


class CVP_OT_PasteVisualObjLocButton(bpy.types.Operator):
    bl_label = "Paste loc"
    bl_idname = "object.paste_visual_location"
    bl_description = "Paste the visual location to active object"

    def execute(self, context):
        scene = bpy.context.scene
        loc = Vector(scene.LastVisualLocation)
        rot = Euler(scene.LastVisualRotation, 'XYZ')
        scale = Vector(scene.LastVisualScale)
        if bpy.context.object.mode == "OBJECT":
            SetVisualObjPos(bpy.context.active_object, loc, rot, scale, True, False, False)
        if bpy.context.object.mode == "POSE":
            SetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone, loc, rot, scale, True, False, False)
        if bpy.context.object.mode == "EDIT":
            SetVisualVertLoc(bpy.context.active_object, loc)
        return {'FINISHED'}


class CVP_OT_PasteVisualObjRotButton(bpy.types.Operator):
    bl_label = "Paste rot"
    bl_idname = "object.paste_visual_rotation"
    bl_description = "Paste the visual rotation to active object"

    def execute(self, context):
        scene = bpy.context.scene
        loc = Vector(scene.LastVisualLocation)
        rot = Euler(scene.LastVisualRotation, 'XYZ')
        scale = Vector(scene.LastVisualScale)
        obj = bpy.context.active_object
        if bpy.context.object.mode == "OBJECT":
            SetVisualObjPos(obj, loc, rot, scale, False, True, False)
        if bpy.context.object.mode == "POSE":
            bone = bpy.context.active_pose_bone
            SetVisualBonePos(obj, bone, loc, rot, scale, False, True, False)
        return {'FINISHED'}


class CVP_OT_PasteObjScaleButton(bpy.types.Operator):
    bl_label = "Paste scale"
    bl_idname = "object.paste_scale"
    bl_description = "Paste the scale to active object"

    def execute(self, context):
        scene = bpy.context.scene
        loc = Vector(scene.LastVisualLocation)
        rot = Euler(scene.LastVisualRotation, 'XYZ')
        scale = Vector(scene.LastVisualScale)
        obj = bpy.context.active_object
        if bpy.context.object.mode == "OBJECT":
            SetVisualObjPos(obj, loc, rot, scale, False, False, True)
        if bpy.context.object.mode == "POSE":
            bone = bpy.context.active_pose_bone
            SetVisualBonePos(obj, bone, loc, rot, scale, False, False, True)
        return {'FINISHED'}


class CVP_OT_PasteVisualObjPosButton(bpy.types.Operator):
    bl_label = "Paste all"
    bl_idname = "object.paste_visual_all"
    bl_description = "Paste the visual position to active object"

    def execute(self, context):
        scene = bpy.context.scene
        loc = Vector(scene.LastVisualLocation)
        rot = Euler(scene.LastVisualRotation, 'XYZ')
        scale = Vector(scene.LastVisualScale)
        obj = bpy.context.active_object
        if bpy.context.object.mode == "OBJECT":
            SetVisualObjPos(obj, loc, rot, scale, True, True, True)
        if bpy.context.object.mode == "POSE":
            bone = bpy.context.active_pose_bone
            SetVisualBonePos(obj, bone, loc, rot, scale, True, True, True)
        return {'FINISHED'}

# ########################## [UI (Packed)] ###########################


class CVP_PT_VisualPosePacked(bpy.types.Panel):  # Is Export panel

    class SaveCopyPosition(bpy.types.PropertyGroup):
        elementName: StringProperty(default="Unknown")
        location: FloatVectorProperty()
        rotation: FloatVectorProperty()
        scale: FloatVectorProperty()

    bpy.utils.register_class(SaveCopyPosition)
    bpy.types.Scene.CopiedObjects = CollectionProperty(
        type=SaveCopyPosition
        )

    bpy.types.Scene.CopiedBones = CollectionProperty(
        type=SaveCopyPosition
        )

    class SaveCopyVertLoc(bpy.types.PropertyGroup):
        id: IntProperty(name="Index")
        location: FloatVectorProperty(name="location")
    bpy.utils.register_class(SaveCopyVertLoc)

    bpy.types.Scene.CopiedVertex = CollectionProperty(
        type=SaveCopyVertLoc
        )

    bl_idname = "CVP_PT_VisualPosePacked"
    bl_label = "Packed"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Copy visual position"

    def draw(self, context):
        scn = context.scene
        layout = self.layout

        text = layout.row()
        text.label(text="Copy visual positions from select", icon='COPYDOWN')
        text.label(text="Paste visual positions to select", icon='PASTEDOWN')
        Buttons = layout.row(align=True).column()
        Button_objs = Buttons.row()
        Button_bones = Buttons.row()
        Button_vertex = Buttons.row()

        Button_objs.operator("object.copy_pack_visual_objs", icon='OBJECT_DATAMODE')
        Button_objs.operator("object.paste_pack_visual_objs", icon='OBJECT_DATAMODE')

        Button_bones.operator("object.copy_pack_visual_bones", icon='POSE_HLT')
        Button_bones.operator("object.paste_pack_visual_bones", icon='POSE_HLT')

        Button_vertex.operator("object.copy_pack_visual_vertex", icon='EDITMODE_HLT')
        Button_vertex.operator("object.paste_pack_visual_vertex", icon='EDITMODE_HLT')

        if bpy.context.object is not None:
            if bpy.context.active_object is not None:
                if bpy.context.object.mode != "OBJECT":
                    Button_objs.enabled = False
                if bpy.context.object.mode != "POSE":
                    Button_bones.enabled = False
                if bpy.context.object.mode != "EDIT":
                    Button_vertex.enabled = False
                if bpy.context.active_object.type != "MESH":
                    Button_vertex.enabled = False
        else:
            Button_objs.enabled = False
            Button_bones.enabled = False
            Button_vertex.enabled = False

# ########################## [Buttons (Packed) ] ###########################


class CVP_OT_CopyVisualObjsPosButton(bpy.types.Operator):
    bl_label = "Copy objs"
    bl_idname = "object.copy_pack_visual_objs"
    bl_description = "Contpy the visual position from selected objects"

    def execute(self, context):
        scene = bpy.context.scene
        scene.CopiedObjects.clear()
        PosList = GetVisualObjsPosPacked(bpy.context.selected_objects)
        for pos in PosList:
            PosProp = scene.CopiedObjects.add()
            PosProp.elementName = pos[0]
            PosProp.location = pos[1]
            PosProp.rotation = pos[2]
            PosProp.scale = pos[3]
        return {'FINISHED'}


class CVP_OT_CopyVisualBonesPosButton(bpy.types.Operator):
    bl_label = "Copy bones"
    bl_idname = "object.copy_pack_visual_bones"
    bl_description = "Contpy the visual position from selected pose bones"

    def execute(self, context):
        scene = bpy.context.scene
        scene.CopiedBones.clear()
        PosList = GetVisualBonesPosPacked(bpy.context.active_object, bpy.context.selected_pose_bones)
        for pos in PosList:
            PosProp = scene.CopiedBones.add()
            PosProp.elementName = pos[0]
            PosProp.location = pos[1]
            PosProp.rotation = pos[2]
            PosProp.scale = pos[3]
        return {'FINISHED'}


class CVP_OT_CopyVisualVertsPosButton(bpy.types.Operator):
    bl_label = "Copy vertex"
    bl_idname = "object.copy_pack_visual_vertex"
    bl_description = "Contpy the visual position from selected mesh vertex"

    def execute(self, context):
        scene = bpy.context.scene
        scene.CopiedVertex.clear()
        PosList = []
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        for vert in bm.verts:
            if vert.select:
                # v.co.x = 0
                ref = vert.index
                PosList.append((ref, vert.co))
                print(ref)
        for pos in PosList:
            id = pos[0]
            prop = scene.CopiedVertex.add()
            prop.id = id
            prop.location = pos[1]
        return {'FINISHED'}


class CVP_OT_PasteVisualObjsPosButton(bpy.types.Operator):
    bl_label = "Paste objs"
    bl_idname = "object.paste_pack_visual_objs"
    bl_description = "Paste the visual position to selected objects"

    def execute(self, context):
        scene = bpy.context.scene
        PosList = []
        for co in scene.CopiedObjects:
            PosList.append((co.elementName, co.location, co.rotation, co.scale))
        SetVisualObjsPosPacked(bpy.context.selected_objects, PosList, True, True, True)
        return {'FINISHED'}


class CVP_OT_PasteVisualBonesPosButton(bpy.types.Operator):
    bl_label = "Paste bones"
    bl_idname = "object.paste_pack_visual_bones"
    bl_description = "Paste the visual position to selected pose bones"

    def execute(self, context):
        scene = bpy.context.scene
        PosList = []
        for co in scene.CopiedBones:
            PosList.append((co.elementName, co.location, co.rotation, co.scale))
        SetVisualBonesPosPacked(bpy.context.active_object, bpy.context.selected_pose_bones, PosList, True, True, True)
        return {'FINISHED'}


class CVP_OT_PasteVisualVertsPosButton(bpy.types.Operator):
    bl_label = "Paste vertex"
    bl_idname = "object.paste_pack_visual_vertex"
    bl_description = "Paste the visual position to selected mesh vertex"

    def execute(self, context):
        scene = bpy.context.scene
        PosList = []
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        for cb in scene.CopiedVertex:
            for vert in bm.verts:
                if vert.select:
                    if vert.index == cb.id:
                        vert.co = cb.location
                        print("VertMove")
        bmesh.update_edit_mesh(me)
        me.update()
        return {'FINISHED'}

# ########################## [Function] ###########################


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
    mat_loc = Matrix.Translation(loc)
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
    loc = matrix_Pose @ Vector((0, 0, 0))
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
    mat_loc = Matrix.Translation(loc)
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
        TargetBone = FindItemInListByName(pl[0], TargetObjs)
        if TargetBone is not None:
            loc = Vector(pl[1])
            rot = Euler(pl[2], 'XYZ')
            scale = Vector(pl[3])
            SetVisualObjPos(TargetBone, loc, rot, scale, UseLoc, UseRot, UseScale)


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
            loc = Vector(pl[1])
            rot = Euler(pl[2], 'XYZ')
            scale = Vector(pl[3])
            SetVisualBonePos(obj, TargetBone, loc, rot, scale, UseLoc, UseRot, UseScale)

# ############################[...]#############################


classes = (

    CVP_OT_CopyVisualObjLocButton,
    CVP_OT_CopyVisualObjRotButton,
    CVP_OT_CopyObjScaleButton,
    CVP_OT_CopyVisualObjPosButton,
    CVP_OT_PasteVisualObjLocButton,
    CVP_OT_PasteVisualObjRotButton,
    CVP_OT_PasteObjScaleButton,
    CVP_OT_PasteVisualObjPosButton,

    CVP_PT_VisualPoseOneByOne,

    CVP_OT_CopyVisualObjsPosButton,
    CVP_OT_CopyVisualBonesPosButton,
    CVP_OT_CopyVisualVertsPosButton,
    CVP_OT_PasteVisualObjsPosButton,
    CVP_OT_PasteVisualBonesPosButton,
    CVP_OT_PasteVisualVertsPosButton,

    CVP_PT_VisualPosePacked,
    # CVP_PT_VisualPosePacked.SaveCopyPosition,
    # CVP_PT_VisualPosePacked.SaveCopyVertLoc,
)

register, unregister = bpy.utils.register_classes_factory(classes)
