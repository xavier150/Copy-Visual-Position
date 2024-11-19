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