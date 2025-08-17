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


def draw_ui(layout: bpy.types.UILayout, context: bpy.types.Context):
    scene = context.scene
    Button_vertex = layout.row()
    Button_vertex.operator("object.copy_pack_visual_vertex", icon='EDITMODE_HLT')
    Button_vertex.operator("object.paste_pack_visual_vertex", icon='EDITMODE_HLT')

    if bpy.context.object is None:
        Button_vertex.enabled = False
        
    if bpy.context.active_object is not None:
            if bpy.context.object.mode != "EDIT":
                Button_vertex.enabled = False
            if bpy.context.active_object.type != "MESH":
                 Button_vertex.enabled = False

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
