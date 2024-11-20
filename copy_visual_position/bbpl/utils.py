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

import json
import copy
import bpy
import mathutils

def select_specific_object(obj: bpy.types.Object):
    """
    Selects a specific object in Blender.

    Args:
        obj (bpy.types.Object): The object to be selected.

    Returns:
        None
    """

    bpy.ops.object.select_all(action='DESELECT')
    if obj.name in bpy.context.window.view_layer.objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

class UserArmatureDataSave():
    """
    Manager for saving and resetting an armature.
    """
        
    def __init__(self, armature):
        # Select
        self.armature = armature

        # Stats
        # Data
        self.use_mirror_x = False

    def save_current_armature(self):
        """
        Save the current armature data.
        """
        if self.armature is None:
            return
        # Select
        # Stats
        # Data
        self.use_mirror_x = self.armature.data.use_mirror_x

    def reset_armature_at_save(self):
        """
        Reset the armature to the state at the last save.
        """
        if self.armature is None:
            return

        # Select
        # Stats
        # Data
        self.armature.data.use_mirror_x = self.use_mirror_x

def mode_set_on_target(target_object=None, target_mode='OBJECT'):
    """
    Set the target object to the specified mode.
    """
    # Exit current mode
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    if target_object:
        target_object.select_set(state=True)
        bpy.context.view_layer.objects.active = target_object

    # Enter new mode
    if bpy.context.active_object:
        bpy.ops.object.mode_set(mode=target_mode)
        return True
    return False

def safe_mode_set(target_mode='OBJECT', obj=None):
    """
    Set the mode of the target object to the specified mode if possible.
    """
    if bpy.ops.object.mode_set.poll():
        if obj:
            if obj.mode != target_mode:
                bpy.ops.object.mode_set(mode=target_mode)
                return True
        else:
            bpy.ops.object.mode_set(mode=target_mode)
            return True

    return False

def json_list(string):
    """
    Convert a JSON string to a list of dictionaries.
    """
    if string is None or string == "":
        return []

    jdata = json.loads(string)
    return list(jdata)

def clear_driver_var(d):
    """
    Clear all variables from a driver.
    """
    #d.variables.clear()
    for var in d.variables:
        d.variables.remove(var)

def update_bone_rot_mode(armature, bone_name, rotation_mode):
    """
    Update the rotation mode of a specific bone in an armature.
    """
    armature.pose.bones[bone_name].rotation_mode = rotation_mode

def get_visual_bone_pos(obj, bone):
    """
    Get the visual position, rotation, and scale of a bone in object space.
    """
    matrix_pose = obj.matrix_world @ bone.matrix
    loc = matrix_pose @ mathutils.Vector((0, 0, 0))
    rot = matrix_pose.to_euler()
    scale = bone.scale
    return loc, rot, scale

def get_visual_bones_pos_packed(obj, target_bones):
    """
    Get the visual positions, rotations, and scales of multiple bones in object space and pack them into a list.
    """
    position_list = []
    for bone in target_bones:
        loc, rot, scale = get_visual_bone_pos(obj, bone)
        position_list.append((bone.name, loc, rot, scale))
    return position_list

def apply_real_matrix_world_bones(bone, obj, matrix):
    """
    Apply the real matrix world to a bone, considering constraints.
    """
    for cons in bone.constraints:
        if cons.type == "CHILD_OF" and not cons.mute and cons.target is not None:
            child = cons.inverse_matrix
            if cons.target.type == "ARMATURE":
                parent = obj.matrix_world @ obj.pose.bones[cons.subtarget].matrix
            else:
                parent = cons.target.matrix_world
            bone.matrix = obj.matrix_world.inverted() @ (child.inverted() @ parent.inverted() @ matrix)
            return
    bone.matrix = obj.matrix_world.inverted() @ matrix

def set_visual_bone_pos(obj, bone, loc, rot, scale, use_loc, use_rot, use_scale):
    """
    Set the visual position, rotation, and scale of a bone, allowing control over which values to apply.
    """
    # Save
    base_loc = copy.deepcopy(bone.location)
    base_scale = copy.deepcopy(bone.scale)
    rot_mode_base = copy.deepcopy(bone.rotation_mode)
    base_rot = copy.deepcopy(bone.rotation_euler)
    base_quaternion = copy.deepcopy(bone.rotation_quaternion)

    # ApplyPos
    mat_loc = mathutils.Matrix.Translation(loc)
    mat_rot = rot.to_matrix().to_4x4()
    matrix = mat_loc @ mat_rot
    apply_real_matrix_world_bones(bone, obj, matrix)
    bone.scale = scale

    # ResetNotDesiredValue
    if not use_loc:
        bone.location = base_loc
    if not use_rot:
        bone.rotation_euler = base_rot
        bone.rotation_quaternion = base_quaternion
        bone.rotation_mode = rot_mode_base
    if not use_scale:
        bone.scale = base_scale

def find_item_in_list_by_name(item, lst):
    """
    Find an item in a list by its name.
    """
    for target_item in lst:
        if target_item.name == item:
            return target_item
    return None

def set_visual_bones_pos_packed(obj, target_bones, position_list, use_loc, use_rot, use_scale):
    """
    Set the visual positions, rotations, and scales of multiple bones using a packed position list,
    allowing control over which values to apply.
    """
    for pl in position_list:
        target_bone = find_item_in_list_by_name(pl[0], target_bones)
        if target_bone is not None:
            loc = mathutils.Vector(pl[1])
            rot = mathutils.Euler(pl[2], 'XYZ')
            scale = mathutils.Vector(pl[3])
            set_visual_bone_pos(obj, target_bone, loc, rot, scale, use_loc, use_rot, use_scale)

def get_safe_collection(collection_name):
    """
    Get an existing collection with the given name, or create a new one if it doesn't exist.
    """
    if collection_name in bpy.data.collections:
        my_col = bpy.data.collections[collection_name]
    else:
        my_col = bpy.data.collections.new(collection_name)
    return my_col

def get_recursive_layer_collection(layer_collection):
    """
    Get all recursive child collections of a layer collection.
    """
    all_childs = []
    for child in layer_collection.children:
        all_childs.append(child)
        all_childs += get_recursive_layer_collection(child)
    return all_childs

def set_collection_exclude(collection, exclude):
    """
    Set the exclude property for a collection in all view layers.
    """
    scene = bpy.context.scene
    for vl in scene.view_layers:
        for layer in get_recursive_layer_collection(vl.layer_collection):
            if layer.collection == collection:
                layer.exclude = exclude

def get_rig_collection(armature, col_type="RIG"):
    """
    Get the rig collection for an armature, optionally creating additional sub-collections based on col_type.
    """
    #TO DO: Move this in Modular Auto Rig Addon.
    rig_col = get_safe_collection(armature.users_collection[0].name)

    if col_type == "RIG":
        return rig_col
    elif col_type == "SHAPE":
        shape_col = get_safe_collection(armature.name + "_RigShapes")
        if shape_col.name not in rig_col.children:
            rig_col.children.link(shape_col)
        return shape_col
    elif col_type == "CURVE":
        curve_col = get_safe_collection(armature.name + "_RigCurves")
        if curve_col.name not in rig_col.children:
            rig_col.children.link(curve_col)
        return curve_col
    elif col_type == "CAMERA":
        camera_col = get_safe_collection(armature.name + "_RigCameras")
        if camera_col.name not in rig_col.children:
            rig_col.children.link(camera_col)
        return camera_col
    else:
        print("In get_rig_collection() " + col_type + " not found!")

def get_vertex_colors(obj):
    """
    Get the vertex colors of an object.
    """
    if bpy.app.version >= (3, 2, 0):
        return obj.data.color_attributes
    else:
        return obj.data.vertex_colors

def get_vertex_colors_render_color_index(obj):
    """
    Get the render color index of the vertex colors of an object.
    """
    if bpy.app.version >= (3, 2, 0):
        return obj.data.color_attributes.render_color_index
    else:
        for index, vertex_color in enumerate(obj.data.vertex_colors):
            if vertex_color.active_render:
                return index

def get_vertex_color_active_color_index(obj):
    """
    Get the active color index of the vertex colors of an object.
    """
    if bpy.app.version >= (3, 2, 0):
        return obj.data.color_attributes.active_color_index
    else:
        return obj.data.vertex_colors.active_index

def get_layer_collections_recursive(layer_collection):
    """
    Get all recursive child layer collections of a layer collection.
    """
    layer_collections = []
    layer_collections.append(layer_collection)  # Add current
    for child_col in layer_collection.children:
        layer_collections.extend(get_layer_collections_recursive(child_col))  # Add child collections recursively

    return layer_collections

def get_mirror_object_name(original_objects):
    """
    Get the mirror object name for the given objects(s).
    """
    objects = []
    new_objects = []

    if not isinstance(original_objects, list):
        objects = [original_objects]  # Convert to list
    else:
        objects = original_objects

    def try_to_invert_bones(bone):
        def invert(bone, old, new):
            if bone.endswith(old):
                new_object_name = bone[:-len(old)]
                new_object_name = new_object_name + new
                return new_object_name
            return None

        change = [
            ["_l", "_r"],
            ["_L", "_R"]
        ]
        for c in change:
            a = invert(bone, c[0], c[1])
            if a:
                return a
            b = invert(bone, c[1], c[0])
            if b:
                return b

        # Return original If no invert found.
        return bone

    for bone in objects:
        new_objects.append(try_to_invert_bones(bone))

    # Can return same bone when don't found mirror
    if not isinstance(original_objects, list):
        return new_objects[0]
    else:
        return new_objects


class SaveTransformObject():
    def __init__(self, obj: bpy.types.Object):
        self.init_object = obj
        self.transform_matrix = obj.matrix_world.copy()

    def reset_object_transform(self):
        self.init_object.matrix_world = self.transform_matrix

    def apply_object_transform(self, obj):
        obj.matrix_world = self.transform_matrix

def make_override_library_object(obj):
    select_specific_object(obj)
    bpy.ops.object.make_override_library()

def recursive_delete_collection(collection: bpy.types.Collection):
    """
    Recursively deletes a Blender collection and its contents, including objects and their data,
    as well as any child collections.

    Parameters:
    - collection (bpy.types.Collection): The Blender collection to be deleted.

    Returns:
    None
    """
    # First, prepare a list of objects and their data to remove from the collection
    objects_to_remove = [obj for obj in collection.objects]
    data_to_remove = [obj.data for obj in collection.objects if obj.data is not None]

    # Use Blender's batch_remove to efficiently delete objects and their data
    bpy.data.batch_remove(objects_to_remove)
    bpy.data.batch_remove(data_to_remove)
    
    # Recursively delete any child collections
    for sub_collection in collection.children:
        recursive_delete_collection(sub_collection)
    
    # Finally, delete the collection itself
    if collection.name in bpy.data.collections:
        bpy.data.collections.remove(collection)

class SaveUserRenderSimplify():
    def __init__(self):
        self.use_simplify = bpy.context.scene.render.use_simplify

    def LoadUserRenderSimplify(self):
        bpy.context.scene.render.use_simplify = self.use_simplify

class SaveObjectReferanceUser():
    """
    This class is used to save and update references to an object in constraints 
    across all bones in all armatures within a Blender scene.
    """

    def __init__(self):
        """
        Initializes the instance with an empty list to store constraints using the specified object.
        """
        self.using_constraints = []

    def save_refs_from_object(self, targe_obj: bpy.types.Object):
        """
        Scans all objects in the Blender scene to find and save constraints in armature bones
        that reference the specified object.

        :param obj: The target bpy.types.Object to find references to.
        """
        scene = bpy.context.scene
        for obj in scene.objects:
            if obj.type == 'ARMATURE':
                for bone in obj.pose.bones:
                    for contrainte in bone.constraints:
                        if hasattr(contrainte, 'target') and contrainte.target and contrainte.target.name == targe_obj.name:
                            constraint_info = {
                                'armature_object': obj.name,
                                'bone': bone.name,
                                'constraint': contrainte.name
                            }
                            self.using_constraints.append(constraint_info)
    
    def update_refs_with_object(self, targe_obj: bpy.types.Object):
        """
        Updates all previously found constraints to reference a new object.

        :param obj: The new bpy.types.Object to be used as the target for the saved constraints.
        """
        scene = bpy.context.scene
        for info in self.using_constraints:
            if info['armature_object'] in scene.objects:
                armature_object = scene.objects.get(info['armature_object'])
                if info['bone'] in armature_object.pose.bones:
                    bone = armature_object.pose.bones[info['bone']]
                    if info['constraint'] in bone.constraints:
                        constraint = bone.constraints[info['constraint']]
                        constraint.target = targe_obj

def active_mode_is(targetMode):
    # Return True is active obj mode == targetMode
    obj = bpy.context.active_object
    if obj is not None:
        if obj.mode == targetMode:
            return True
    return False

def active_type_is(targetType):
    # Return True is active obj type == targetType
    obj = bpy.context.active_object
    if obj is not None:
        if obj.type == targetType:
            return True
    return False

def active_type_is_not(targetType):
    # Return True is active obj type != targetType
    obj = bpy.context.active_object
    if obj is not None:
        if obj.type != targetType:
            return True
    return False

def found_type_in_selection(targetType, include_active=True):
    # Return True if a specific type is found in current user selection
    select = bpy.context.selected_objects
    if not include_active:
        if bpy.context.active_object:
            if bpy.context.active_object in select:
                select.remove(bpy.context.active_object)

    for obj in select:
        if obj.type == targetType:
            return True
    return False

def get_bone_path(armature: bpy.types.Object, start_bone_name: str, end_bone_name: str):
    """
    Returns a list of bone names between start_bone and end_bone in an armature.
    
    :param armature: The armature object.
    :param start_bone_name: The name of the starting bone.
    :param end_bone_name: The name of the ending bone.
    :return: List of bone names between start_bone and end_bone, or an empty list if no path is found.
    """

    # Access bones directly.
    if armature.mode == 'EDIT':
        bones = armature.data.edit_bones
    else:
        bones = armature.data.bones

    # Initialize the bones
    start_bone = bones[start_bone_name]
    end_bone = bones[end_bone_name]

    # Depth-First Search to find the path from start_bone to end_bone
    def find_path(current_bone, path):
        path.append(current_bone.name)

        # Check if we've reached the end bone
        if current_bone == end_bone:
            return path

        # Explore each child recursively
        for child in current_bone.children:
            result = find_path(child, path[:])  # Use a copy of the current path
            if result:  # If a valid path is found, return it
                return result
        
        return None  # Return None if no path is found from this branch

    # Start the recursive search
    all_bones = find_path(start_bone, [])
    return all_bones

    
def get_bone_path_to_end(armature: bpy.types.Object, start_bone_name: str):
    """
    Returns a list of bone names from the start_bone to the last child in a chain.
    
    :param armature: The armature object.
    :param start_bone_name: The name of the starting bone.
    :return: List of bone names from start_bone to the last child.
    """

    # Access bones directly.
    if armature.mode == 'EDIT':
        bones = armature.data.edit_bones
    else:
        bones = armature.data.bones

    # Initialize the bones
    start_bone = bones[start_bone_name]

    # Traverse bones from start_bone to the last child in the chain
    current_bone = start_bone
    bone_path = [current_bone.name]

    while current_bone.children:
        # Use first child only
        current_bone = current_bone.children[0]
        bone_path.append(current_bone.name)

    return bone_path

def get_bone_and_children(armature: bpy.types.Object, start_bone_name: str):
    """
    Returns a list of all descendant bones of the specified start_bone, including all children recursively.
    
    :param armature: The armature object.
    :param start_bone_name: The name of the starting bone.
    :return: List of bone names, including the start bone and all its descendants.
    """

    # Access bones directly.
    if armature.mode == 'EDIT':
        bones = armature.data.edit_bones
    else:
        bones = armature.data.bones

    # Initialize the bones
    bones = armature.data.edit_bones
    start_bone = bones.get(start_bone_name)
    

    # Recursive function to collect all children bones
    def collect_children(bone):
        bone_list = [bone.name]
        for child in bone.children:
            bone_list.extend(collect_children(child))
        return bone_list

    # Get all bones starting from the start_bone
    all_bones = collect_children(start_bone)
    return all_bones
