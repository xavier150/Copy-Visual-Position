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
from typing import List
from .. import utils

class UserSelectSave():
    """
    Manager for user selection.
    """

    def __init__(self):
        # Select
        self.user_active = None
        self.user_active_name = ""
        self.user_selecteds: List[bpy.types.Object] = []
        self.user_selected_names: List[str] = []

        # Stats
        self.user_mode = None

    def save_current_select(self):
        """
        Save user selection.
        """

        # Save data (This can take time)

        # Select
        self.user_active = bpy.context.active_object  # Save current active object
        if self.user_active:
            self.user_active_name = self.user_active.name

        self.user_selecteds = bpy.context.selected_objects  # Save current selected objects
        self.user_selected_names = [obj.name for obj in bpy.context.selected_objects]

    def reset_select(self, use_names: bool = False):
        """
        Reset user selection at the last save.
        """

        scene = bpy.context.scene
        self.save_mode(use_names)
        utils.safe_mode_set("OBJECT", bpy.ops.object)
        bpy.ops.object.select_all(action='DESELECT')

        if use_names:
            for obj in scene.objects:
                if obj.name in self.user_selected_names:
                    if obj.name in bpy.context.view_layer.objects:
                        scene.objects.get(obj.name).select_set(True)  # Use the name because can be duplicated name

            if self.user_active_name != "":
                if self.user_active_name in scene.objects:
                    if self.user_active_name in bpy.context.view_layer.objects:
                        bpy.context.view_layer.objects.active = scene.objects.get(self.user_active_name)
        
        
        else:
            for obj in scene.objects:  # Resets previous selected object if still exist
                if obj in self.user_selecteds:
                    obj.select_set(True)

            bpy.context.view_layer.objects.active = self.user_active

        self.reset_mode_at_save()

    def save_mode(self, use_names: bool = False):
        """
        Save user mode.
        """

        user_active = self.get_user_active(use_names)
        if user_active:
            if bpy.ops.object.mode_set.poll():
                self.user_mode = user_active.mode  # Save current mode

    def reset_mode_at_save(self):
        """
        Reset user mode at the last save.
        """
        if self.user_mode:
            utils.safe_mode_set(self.user_mode, bpy.ops.object)

    def get_user_active(self, use_names: bool = False):
        scene = bpy.context.scene
        if use_names:
            if self.user_active_name != "":
                if self.user_active_name in scene.objects:
                    if self.user_active_name in bpy.context.view_layer.objects:
                        return scene.objects.get(self.user_active_name)
            return None
        else:
            return self.user_active