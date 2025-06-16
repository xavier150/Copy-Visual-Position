# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================

# ----------------------------------------------
#  BBPL -> BleuRaven Blender Python Library
#  BleuRaven.fr
#  XavierLoux.com
# ----------------------------------------------

import bpy
import os
import webbrowser
from . import utils



class CustomOpenTargetWebPage_Operator(bpy.types.Operator):
    bl_label = "Documentation"
    bl_idname = utils.get_open_target_web_page_idname()
    bl_description = "Click for open URL."
    url: bpy.props.StringProperty(default="https://github.com/xavier150/BleuRavenBlenderPythonLibrary")  # type: ignore

    def execute(self, context):
        # Check if the URL starts with http:// or https://
        if self.url.startswith("http://") or self.url.startswith("https://"):
            webbrowser.open(self.url)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Invalid URL. Only HTTP and HTTPS URLs are allowed.")
            return {'CANCELLED'}

def create_doc_operator_class():
    # Create an custom class ussing addon name for avoid name collision.
    CustomOpenTargetWebPage_Operator.__name__ = utils.get_open_target_web_page_class_name()
    return CustomOpenTargetWebPage_Operator

# ----------------- Register ----------------

BBPL_OT_OpenTargetWebPage_CUSTOM_CLASS = None

def init_doc_button():
    global BBPL_OT_OpenTargetWebPage_CUSTOM_CLASS
    if BBPL_OT_OpenTargetWebPage_CUSTOM_CLASS is None:
        BBPL_OT_OpenTargetWebPage_CUSTOM_CLASS = create_doc_operator_class()


init_doc_button()

classes = (
)



def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    global BBPL_OT_OpenTargetWebPage_CUSTOM_CLASS
    bpy.utils.register_class(BBPL_OT_OpenTargetWebPage_CUSTOM_CLASS)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    global BBPL_OT_OpenTargetWebPage_CUSTOM_CLASS
    bpy.utils.unregister_class(BBPL_OT_OpenTargetWebPage_CUSTOM_CLASS)