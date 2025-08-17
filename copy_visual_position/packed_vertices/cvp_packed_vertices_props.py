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
import bmesh

class SaveCopyVertLoc(bpy.types.PropertyGroup):
    id: bpy.props.IntProperty(name="Index")
    location: bpy.props.FloatVectorProperty(name="location")


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
        for pos in PosList:
            id = pos[0]
            prop = scene.CopiedVertex.add()
            prop.id = id
            prop.location = pos[1]
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
        bmesh.update_edit_mesh(me)
        me.update()
        return {'FINISHED'}

classes = (
    SaveCopyVertLoc,
    CVP_OT_CopyVisualVertsPosButton,
    CVP_OT_PasteVisualVertsPosButton,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.CopiedVertex = bpy.props.CollectionProperty(type=SaveCopyVertLoc)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.CopiedVertex