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
import mathutils
from . import cvp_single_object_utils
from .. import cvp_utils


def draw_ui(layout: bpy.types.UILayout, context: bpy.types.Context):
    scene = context.scene

    layout.prop(scene, 'LastVisualLocation')
    layout.prop(scene, 'LastVisualRotation')
    layout.prop(scene, 'LastVisualScale')

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
            scene.LastVisualLocation = cvp_single_object_utils.GetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone)[0]
        if bpy.context.object.mode == "EDIT":
            scene.LastVisualLocation = cvp_single_object_utils.GetVisualVertLoc(bpy.context.active_object)
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
            scene.LastVisualRotation = cvp_single_object_utils.GetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone)[1]
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
            scene.LastVisualScale = cvp_single_object_utils.GetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone)[2]
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
            Trans = cvp_utils.GetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone)
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
        loc = mathutils.Vector(scene.LastVisualLocation)
        rot = mathutils.Euler(scene.LastVisualRotation, 'XYZ')
        scale = mathutils.Vector(scene.LastVisualScale)
        if bpy.context.object.mode == "OBJECT":
            cvp_utils.SetVisualObjPos(bpy.context.active_object, loc, rot, scale, True, False, False)
        if bpy.context.object.mode == "POSE":
            cvp_utils.SetVisualBonePos(bpy.context.active_object, bpy.context.active_pose_bone, loc, rot, scale, True, False, False)
        if bpy.context.object.mode == "EDIT":
            cvp_utils.SetVisualVertLoc(bpy.context.active_object, loc)
        return {'FINISHED'}


class CVP_OT_PasteVisualObjRotButton(bpy.types.Operator):
    bl_label = "Paste rot"
    bl_idname = "object.paste_visual_rotation"
    bl_description = "Paste the visual rotation to active object"

    def execute(self, context):
        scene = bpy.context.scene
        loc = mathutils.Vector(scene.LastVisualLocation)
        rot = mathutils.Euler(scene.LastVisualRotation, 'XYZ')
        scale = mathutils.Vector(scene.LastVisualScale)
        obj = bpy.context.active_object
        if bpy.context.object.mode == "OBJECT":
            cvp_utils.SetVisualObjPos(obj, loc, rot, scale, False, True, False)
        if bpy.context.object.mode == "POSE":
            bone = bpy.context.active_pose_bone
            cvp_utils.SetVisualBonePos(obj, bone, loc, rot, scale, False, True, False)
        return {'FINISHED'}


class CVP_OT_PasteObjScaleButton(bpy.types.Operator):
    bl_label = "Paste scale"
    bl_idname = "object.paste_scale"
    bl_description = "Paste the scale to active object"

    def execute(self, context):
        scene = bpy.context.scene
        loc = mathutils.Vector(scene.LastVisualLocation)
        rot = mathutils.Euler(scene.LastVisualRotation, 'XYZ')
        scale = mathutils.Vector(scene.LastVisualScale)
        obj = bpy.context.active_object
        if bpy.context.object.mode == "OBJECT":
            cvp_utils.SetVisualObjPos(obj, loc, rot, scale, False, False, True)
        if bpy.context.object.mode == "POSE":
            bone = bpy.context.active_pose_bone
            cvp_utils.SetVisualBonePos(obj, bone, loc, rot, scale, False, False, True)
        return {'FINISHED'}


class CVP_OT_PasteVisualObjPosButton(bpy.types.Operator):
    bl_label = "Paste all"
    bl_idname = "object.paste_visual_all"
    bl_description = "Paste the visual position to active object"

    def execute(self, context):
        scene = bpy.context.scene
        loc = mathutils.Vector(scene.LastVisualLocation)
        rot = mathutils.Euler(scene.LastVisualRotation, 'XYZ')
        scale = mathutils.Vector(scene.LastVisualScale)
        obj = bpy.context.active_object
        if bpy.context.object.mode == "OBJECT":
            cvp_utils.SetVisualObjPos(obj, loc, rot, scale, True, True, True)
        if bpy.context.object.mode == "POSE":
            bone = bpy.context.active_pose_bone
            cvp_utils.SetVisualBonePos(obj, bone, loc, rot, scale, True, True, True)
        return {'FINISHED'}

classes = (
    CVP_OT_CopyVisualObjLocButton,
    CVP_OT_CopyVisualObjRotButton,
    CVP_OT_CopyObjScaleButton,
    CVP_OT_CopyVisualObjPosButton,
    CVP_OT_PasteVisualObjLocButton,
    CVP_OT_PasteVisualObjRotButton,
    CVP_OT_PasteObjScaleButton,
    CVP_OT_PasteVisualObjPosButton,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
