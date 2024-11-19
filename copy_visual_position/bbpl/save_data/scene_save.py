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
from typing import List, TYPE_CHECKING
from . import select_save
from .. import utils

class SavedObject():
    """
    Saved data from a blender object.
    """

    def __init__(self, obj: bpy.types.Object):
        if obj:
            self.ref = obj
            self.name = obj.name
            self.select = obj.select_get()
            self.hide = obj.hide_get()
            self.hide_select = obj.hide_select
            self.hide_viewport = obj.hide_viewport

    def get_obj(self, use_names: bool = False)-> bpy.types.Object:  
        scene = bpy.context.scene  
        if use_names:
            if self.name != "":
                if self.name in scene.objects:
                    if self.name in bpy.context.view_layer.objects:
                        return scene.objects[self.name]
            return None
        else:
            return self.ref




class SavedBones():
    """
    Saved data from a blender armature bone.
    """

    def __init__(self, bone):
        if bone:
            self.name = bone.name
            self.select = bone.select
            self.hide = bone.hide


class SavedCollection():
    """
    Saved data from a blender collection.
    """

    def __init__(self, col :bpy.types.Collection):
        if col:
            self.ref:bpy.types.Collection = col
            self.name = col.name
            self.hide_select = col.hide_select
            self.hide_viewport = col.hide_viewport

    def get_col(self, use_names: bool = False)-> bpy.types.Collection: 
        if use_names:
            if self.name != "":
                if self.name in bpy.data.collections:
                        return bpy.data.collections[self.name]
            return None
        else:
            return self.ref

class SavedViewLayerChildren():
    """
    Saved data from a blender ViewLayerChildren.
    """

    def __init__(self, vlayer :bpy.types.ViewLayer, child_col :bpy.types.LayerCollection):
        if child_col:
            self.vlayer_name = vlayer.name
            self.name = child_col.name
            self.exclude = child_col.exclude
            self.hide_viewport = child_col.hide_viewport


class UserSceneSave():
    """
    Manager for saving and resetting the user scene.
    """

    def __init__(self):
        # Select
        self.user_select_class = select_save.UserSelectSave()

        self.user_bone_active = None
        self.user_bone_active_name = ""

        # Stats
        self.user_mode = None
        self.use_simplify = False

        # Data
        self.objects: List[SavedObject] = []
        self.object_bones: List[SavedBones] = []
        self.collections: List[SavedCollection] = []
        self.view_layer_collections: List[SavedViewLayerChildren] = []
        self.action_names: List[str] = []
        self.collection_names: List[str] = []

    def save_current_scene(self):
        """
        Save the current scene data.
        """
        # Save data (This can take time)
        scene = bpy.context.scene

        # Select
        self.user_select_class.save_current_select()

        # Stats
        if self.user_select_class.user_active:
            if bpy.ops.object.mode_set.poll():
                self.user_mode = self.user_select_class.user_active.mode  # Save current mode
        self.use_simplify = bpy.context.scene.render.use_simplify

        # Data
        for obj in scene.objects:
            self.objects.append(SavedObject(obj))
        for col in bpy.data.collections:
            self.collections.append(SavedCollection(col))
        for vlayer in scene.view_layers:
            layer_collections = utils.get_layer_collections_recursive(vlayer.layer_collection)
            for layer_collection in layer_collections:
                self.view_layer_collections.append(SavedViewLayerChildren(vlayer, layer_collection))
        for action in bpy.data.actions:
            self.action_names.append(action.name)
        for collection in bpy.data.collections:
            self.collection_names.append(collection.name)

        # Data for armature
        if self.user_select_class.user_active:
            if self.user_select_class.user_active.type == "ARMATURE":
                if self.user_select_class.user_active.data.bones.active:
                    self.user_bone_active = self.user_select_class.user_active.data.bones.active
                    self.user_bone_active_name = self.user_select_class.user_active.data.bones.active.name
                for bone in self.user_select_class.user_active.data.bones:
                    self.object_bones.append(SavedBones(bone))

    def reset_select(self, use_names: bool = False):
        """
        Reset the user selection based on object references.
        """
        self.user_select_class.reset_select(use_names)
        self.reset_bones_select(use_names)

    def reset_bones_select(self, use_names: bool = False):
        """
        Reset bone selection by name (works only in pose mode).
        """
        # Work only in pose mode!
        if len(self.object_bones) > 0:
            user_active = self.user_select_class.get_user_active(use_names)
            if user_active:
                if bpy.ops.object.mode_set.poll():
                    if user_active.mode == "POSE":
                        bpy.ops.pose.select_all(action='DESELECT')
                        for bone in self.object_bones:
                            if bone.select:
                                if bone.name in user_active.data.bones:
                                    user_active.data.bones[bone.name].select = True

                        if self.user_bone_active_name is not None:
                            if self.user_bone_active_name in user_active.data.bones:
                                new_active = user_active.data.bones[self.user_bone_active_name]
                                user_active.data.bones.active = new_active

    def reset_mode_at_save(self):
        """
        Reset the user mode at the last save.
        """
        if self.user_mode:
            utils.safe_mode_set(self.user_mode, bpy.ops.object)

    def reset_scene_at_save(self, print_removed_items = False, use_names: bool = False):
        """
        Reset the user scene to at the last save.
        """
        scene = bpy.context.scene
        self.reset_mode_at_save()

        bpy.context.scene.render.use_simplify = self.use_simplify

        # Reset hide and select
        for obj in self.objects:
            try:
                obj_ref = obj.get_obj(use_names)
                if obj_ref:
                    if obj_ref.hide_select != obj.hide_select:
                        obj_ref.hide_select = obj.hide_select
                    if obj_ref.hide_viewport != obj.hide_viewport:
                        obj_ref.hide_viewport = obj.hide_viewport
                    if obj_ref.hide_get() != obj.hide:
                        obj_ref.hide_set(obj.hide)
                else:
                    if print_removed_items:
                        print(f"/!\\ {obj.name} not found.")
            except ReferenceError:
                if print_removed_items:
                    print(f"/!\\ object {obj.name} has been removed.")

        # Reset hide and select (bpy.data.collections)
        for col in self.collections:
            try:
                col_ref = col.get_col(use_names)
                if col_ref:
                    if col_ref.hide_select != col.hide_select:
                        col_ref.hide_select = col.hide_select
                    if col_ref.hide_viewport != col.hide_viewport:
                        col_ref.hide_viewport = col.hide_viewport
                else:
                    if print_removed_items:
                        print(f"/!\\ {col.name} not found.")
            except ReferenceError:
                if print_removed_items:
                    print(f"/!\\ collection {col.name} has been removed.")

        # Reset hide and viewport (collections from view_layers)
        for vlayer in scene.view_layers:
            layer_collections = utils.get_layer_collections_recursive(vlayer.layer_collection)

            def get_layer_collection_in_list(name, collections) -> bpy.types.LayerCollection:
                for layer_collection in collections:
                    if layer_collection.name == name:
                        return layer_collection

            for view_layer_collection in self.view_layer_collections:
                if view_layer_collection.vlayer_name == vlayer.name:
                    layer_collection = get_layer_collection_in_list(view_layer_collection.name, layer_collections)
                    if layer_collection:
                        if layer_collection.exclude != view_layer_collection.exclude:
                            layer_collection.exclude = view_layer_collection.exclude
                        if layer_collection.hide_viewport != view_layer_collection.hide_viewport:
                            layer_collection.hide_viewport = view_layer_collection.hide_viewport

