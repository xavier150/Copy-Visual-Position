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
from . import cvp_packed_objs_utils
from .. import cvp_utils

class SaveCopyObjPosition(bpy.types.PropertyGroup):
    elementName: bpy.props.StringProperty(default="Unknown")
    location: bpy.props.FloatVectorProperty()
    rotation: bpy.props.FloatVectorProperty()
    scale: bpy.props.FloatVectorProperty()


class CVP_OT_CopyVisualObjsPosButton(bpy.types.Operator):
    bl_label = "Copy objs"
    bl_idname = "object.copy_pack_visual_objs"
    bl_description = "Contpy the visual position from selected objects"

    def execute(self, context):
        scene = bpy.context.scene
        scene.CopiedObjects.clear()
        PosList = cvp_packed_objs_utils.GetVisualObjsPosPacked(bpy.context.selected_objects)
        for pos in PosList:
            PosProp = scene.CopiedObjects.add()
            PosProp.elementName = pos[0]
            PosProp.location = pos[1]
            PosProp.rotation = pos[2]
            PosProp.scale = pos[3]
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
        cvp_packed_objs_utils.SetVisualObjsPosPacked(bpy.context.selected_objects, PosList, True, True, True)
        return {'FINISHED'}

classes = (
    SaveCopyObjPosition,
    CVP_OT_CopyVisualObjsPosButton,
    CVP_OT_PasteVisualObjsPosButton,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.CopiedObjects = bpy.props.CollectionProperty(type=SaveCopyObjPosition)



def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.CopiedObjects
