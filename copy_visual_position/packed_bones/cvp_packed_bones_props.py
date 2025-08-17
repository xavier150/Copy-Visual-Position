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
from . import cvp_packed_bones_utils

class SaveCopyBonePosition(bpy.types.PropertyGroup):
    elementName: bpy.props.StringProperty(default="Unknown")
    location: bpy.props.FloatVectorProperty()
    rotation: bpy.props.FloatVectorProperty()
    scale: bpy.props.FloatVectorProperty()


class CVP_OT_CopyVisualBonesPosButton(bpy.types.Operator):
    bl_label = "Copy bones"
    bl_idname = "object.copy_pack_visual_bones"
    bl_description = "Contpy the visual position from selected pose bones"

    def execute(self, context):
        scene = bpy.context.scene
        scene.CopiedBones.clear()
        PosList = cvp_packed_bones_utils.GetVisualBonesPosPacked(bpy.context.active_object, bpy.context.selected_pose_bones)
        for pos in PosList:
            PosProp = scene.CopiedBones.add()
            PosProp.elementName = pos[0]
            PosProp.location = pos[1]
            PosProp.rotation = pos[2]
            PosProp.scale = pos[3]
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
        cvp_packed_bones_utils.SetVisualBonesPosPacked(bpy.context.active_object, bpy.context.selected_pose_bones, PosList, True, True, True)
        return {'FINISHED'}



classes = (
    SaveCopyBonePosition,
    CVP_OT_CopyVisualBonesPosButton,
    CVP_OT_PasteVisualBonesPosButton,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.CopiedBones = bpy.props.CollectionProperty(type=SaveCopyBonePosition)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.CopiedBones