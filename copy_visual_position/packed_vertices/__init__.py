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

from . import cvp_packed_vertices_props
from . import cvp_packed_vertices_ui
from . import cvp_packed_vertices_utils

import importlib
if "cvp_packed_vertices_props" in locals():
    importlib.reload(cvp_packed_vertices_props)
if "cvp_packed_vertices_ui" in locals():
    importlib.reload(cvp_packed_vertices_ui)
if "cvp_packed_vertices_utils" in locals():
    importlib.reload(cvp_packed_vertices_utils)



# ############################[...]#############################


classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    cvp_packed_vertices_props.register()
    cvp_packed_vertices_ui.register()
    


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    cvp_packed_vertices_ui.unregister()
    cvp_packed_vertices_props.unregister()