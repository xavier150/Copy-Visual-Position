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


def draw_ui(layout: bpy.types.UILayout, context: bpy.types.Context):
    scene = context.scene
    Button_objs = layout.row()
    Button_objs.operator("object.copy_pack_visual_objs", icon='OBJECT_DATAMODE')
    Button_objs.operator("object.paste_pack_visual_objs", icon='OBJECT_DATAMODE')

    if bpy.context.object is None:
        Button_objs.enabled = False
        
    if bpy.context.active_object is not None:
            if bpy.context.object.mode != "OBJECT":
                Button_objs.enabled = False
    

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
