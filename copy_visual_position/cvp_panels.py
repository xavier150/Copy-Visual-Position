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
from . import single_object
from . import packed_objs
from . import packed_bones
from . import packed_vertices


class CVP_PT_VisualPoseOneByOne(bpy.types.Panel):  # Is Export panel


    bl_idname = "CVP_PT_VisualPoseOneByOne"
    bl_label = "One by one"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Copy visual position"

    def draw(self, context: bpy.types.Context):
        single_object.cvp_single_object_ui.draw_ui(self.layout, context)



class CVP_PT_VisualPosePacked(bpy.types.Panel):  # Is Export panel


    bl_idname = "CVP_PT_VisualPosePacked"
    bl_label = "Packed"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Copy visual position"

    def draw(self, context):

        layout = self.layout
        text = layout.row()
        text.label(text="Copy visual positions from select", icon='COPYDOWN')
        text.label(text="Paste visual positions to select", icon='PASTEDOWN')

        Buttons = layout.row(align=True).column()
        packed_objs.cvp_packed_objs_ui.draw_ui(Buttons, context)
        packed_bones.cvp_packed_bones_ui.draw_ui(Buttons, context)
        packed_vertices.cvp_packed_vertices_ui.draw_ui(Buttons, context)





classes = (
    CVP_PT_VisualPoseOneByOne,
    CVP_PT_VisualPosePacked,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
