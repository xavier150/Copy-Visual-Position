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
        cvp_utils.SetVisualObjsPosPacked(bpy.context.selected_objects, PosList, True, True, True)
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
