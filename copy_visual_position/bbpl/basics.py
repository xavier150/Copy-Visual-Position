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

import os
import string
import shutil
import bpy
import bmesh
import addon_utils
import pathlib
from typing import Optional


def check_plugin_is_activated(plugin_name):
    """
    Checks if a Blender plugin is activated.

    Args:
        plugin_name (str): The name of the plugin.

    Returns:
        bool: True if the plugin is enabled and loaded, False otherwise.
    """
    is_enabled, is_loaded = addon_utils.check(plugin_name)
    return is_enabled and is_loaded


def checks_relationship(arrayA, arrayB):
    """
    Checks if there is an identical variable between two lists.

    Args:
        arrayA (list): The first list.
        arrayB (list): The second list.

    Returns:
        bool: True if an identical variable exists, False otherwise.
    """

    for a in arrayA:
        for b in arrayB:
            if a == b:
                return True
    return False


def remove_folder_tree(folder):
    """
    Removes a folder and its entire directory tree.

    Args:
        folder (str): The path to the folder to be removed.

    Returns:
        None
    """
    dirig_prefixath = pathlib.Path(folder)
    if dirig_prefixath.exists() and dirig_prefixath.is_dir():
        shutil.rmtree(dirig_prefixath, ignore_errors=True)


def get_childs(obj):
    """
    Retrieves all direct children of an object.

    Args:
        obj (bpy.types.Object): The parent object.

    Returns:
        list: A list of direct children objects.
    """
    scene = bpy.context.scene
    childs_obj = []
    for child_obj in scene.objects:
        if child_obj.library is None:
            parent = child_obj.parent
            if parent is not None:
                if parent.name == obj.name:
                    childs_obj.append(child_obj)

    return childs_obj


def get_armature_root_bone(obj):
    """
    Retrieves the root bone of an armature object.

    Args:
        obj (bpy.types.Object): The armature object to find the root bone for.

    Returns:
        bpy.types.Bone: The root bone of the armature, or None if not found.
    """
    # Vérifie si l'objet est une armature et s'il a des données d'armature
    if obj.type == 'ARMATURE' and obj.data:
        armature = obj.data
        
        # Parcours tous les os de l'armature pour trouver le(s) root(s)
        for bone in armature.bones:
            if bone.parent is None:
                return bone
    return None


def get_armature_root_bone(obj: bpy.types.Object) -> Optional[bpy.types.Bone]:
    """
    Retrieves the root bone of an armature object.

    Args:
        obj (bpy.types.Object): The armature object to find the root bone for.

    Returns:
        bpy.types.Bone: The root bone of the armature, or None if not found.
    """
    if obj.type == 'ARMATURE' and obj.data:
        armature = obj.data
        
        for bone in armature.bones:
            if bone.parent is None:
                return bone
    return None


def get_root_bone_parent(bone: bpy.types.Bone) -> bpy.types.Bone:
    """
    Retrieves the root bone parent of a given bone by traversing the bone's parents.

    Args:
        bone (bpy.types.Bone): The bone to find the root bone parent for.

    Returns:
        bpy.types.Bone: The root bone parent.
    """
    while bone.parent:
        bone = bone.parent
    return bone


def get_first_deform_bone_parent(bone: bpy.types.Bone) -> Optional[bpy.types.Bone]:
    """
    Retrieves the first deform bone parent of a given bone by traversing the bone's parents.

    Args:
        bone (bpy.types.Bone): The bone to find the first deform bone parent for.

    Returns:
        bpy.types.Bone: The first deform bone parent, or None if not found.
    """
    while bone.parent:
        if bone.use_deform:
            return bone
        bone = bone.parent
    return bone if bone.use_deform else None


def get_recursive_childs(target_obj):
    """
    Retrieves all recursive children of an object.

    Args:
        obj (bpy.types.Object): The parent object.

    Returns:
        list: A list of recursive children objects.
    """
    def get_recursive_parent(parent, start_obj):
        if start_obj.parent:
            if start_obj.parent == parent:
                return True
            else:
                if get_recursive_parent(parent, start_obj.parent):
                    return True
        return False

    scene = bpy.context.scene
    save_objs = []
    for obj in scene.objects:
        if get_recursive_parent(target_obj, obj):
            save_objs.append(obj)
    return save_objs


def convert_to_convex_hull(obj):
    """
    Converts an object to a convex hull.

    Args:
        obj (bpy.types.Object): The object to convert.

    Returns:
        None
    """
    mesh = obj.data
    if not mesh.is_editmode:
        bm = bmesh.new()
        bm.from_mesh(mesh)  # Mesh to Bmesh
        bmesh.ops.convex_hull(bm, input=bm.verts, use_existing_faces=True)
        # convex_hull = bmesh.ops.convex_hull(bm, input=bm.verts, use_existing_faces=True)
        # convex_hull = bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)  # BMesh to Mesh


def verify_dirs(directory):
    """
    Checks if a directory exists and creates it if it doesn't.

    Args:
        directory (str): The directory path to check.

    Returns:
        None
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def valid_filename(filename):
    """
    Normalizes a string by removing non-alphanumeric characters for file name use.

    Args:
        filename (str): The input filename.

    Returns:
        str: The normalized filename.
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)
    return filename


def valid_defname(filename):
    """
    Normalizes a string by removing non-alphanumeric characters for function name use.

    Args:
        filename (str): The input filename.

    Returns:
        str: The normalized filename.
    """
    valid_chars = "_%s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)
    return filename


def get_if_action_is_associated(action, bone_names):
    """
    Checks if the given action is associated with any of the specified bone names.

    Args:
        action (bpy.types.Action): The action to check.
        bone_names (list): List of bone names.

    Returns:
        bool: True if the action is associated with any bone in the list, False otherwise.
    """
    for group in action.groups:
        for fcurve in group.channels:
            s = fcurve.data_path
            start = s.find('["')
            end = s.rfind('"]')
            if start > 0 and end > 0:
                substring = s[start+2:end]
                if substring in bone_names:
                    return True
    return False


def get_surface_area(obj):
    """
    Computes the surface area of a mesh object.

    Args:
        obj (bpy.types.Object): The mesh object.

    Returns:
        float: The surface area of the mesh object.
    """
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    area = sum(f.calc_area() for f in bm.faces)
    bm.free()
    return area


def set_windows_clipboard(text):
    """
    Sets the text content to the clipboard.

    Args:
        text (str): The text to be set to the clipboard.

    Returns:
        None
    """
    bpy.context.window_manager.clipboard = text
    # bpy.context.window_manager.clipboard.encode('utf8')

def get_obj_childs(obj):
    # Get all direct childs of a object

    scene = bpy.context.scene
    childs_obj = []
    for childObj in scene.objects:
        if childObj.library is None:
            pare = childObj.parent
            if pare is not None:
                if pare.name == obj.name:
                    childs_obj.append(childObj)

    return childs_obj

def get_recursive_obj_childs(obj, include_self = False):
    # Get all recursive childs of a object
    # include_self is True obj is index 0

    saveObjs = []

    def tryAppend(obj):
        if obj.name in bpy.context.scene.objects:
            saveObjs.append(obj)

    if include_self:
        tryAppend(obj)

    for newobj in get_obj_childs(obj):
        for childs in get_recursive_obj_childs(newobj):
            tryAppend(childs)
        tryAppend(newobj)
    return saveObjs
