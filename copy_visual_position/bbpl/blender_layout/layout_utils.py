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
from typing import Union, Optional

def get_property_name_from_property_group(property_group: bpy.types.PropertyGroup, property_group_instance: type) -> str:
    # Attempts to retrieve the property name from a given PropertyGroup instance
    # by inspecting its owner and matching pointers.
    # I not found better waut to get the property name of a property group...
    # WTF Blender ?

    # For Blender 3.0 and newer
    if bpy.app.version >= (3, 0, 0):
        
        prop_id_name = property_group.id_properties_ensure().name

        def try_get_name_from_prop(test_pro_owner: Union[bpy.types.Node, bpy.types.PropertyGroup]) -> Optional[str]:
            if hasattr(test_pro_owner, prop_id_name):
                test_prop = getattr(test_pro_owner, prop_id_name)
                if isinstance(test_prop, property_group_instance):
                    test_prop: bpy.types.PropertyGroup
                    if test_prop.as_pointer() == property_group.as_pointer():
                        return test_pro_owner.bl_rna.properties[prop_id_name].name  # type: ignore
            return None

        id_data = property_group.id_data

        # FOR NODE TREE
        if isinstance(id_data, bpy.types.NodeTree):

            # Check all nodes
            for node in id_data.nodes:
                result = try_get_name_from_prop(node)
                if result:
                    return result

            # Check all property groups of all nodes
            for node in id_data.nodes:
                for attr_name in dir(node):
                    # Ignore internal properties (starting with "_")
                    if attr_name.startswith("_"):
                        continue

                    try:
                        test_prop_group = getattr(node, attr_name)
                    except Exception:
                        continue

                    # Checks only instance of PropertyGroup
                    if isinstance(test_prop_group, bpy.types.PropertyGroup):
                        result = try_get_name_from_prop(test_prop_group)
                        if result:
                            return result

        # FOR OBJECT
        if isinstance(id_data, bpy.types.Object):  # type: ignore
            id_data: bpy.types.Object
            # @TODO    

        # FOR OTHER (Try direct read)
        if prop_id_name in id_data.bl_rna.properties:
            return id_data.bl_rna.properties[prop_id_name].name  # type: ignore
        
        # Name not found so return id name
        return prop_id_name

    else:
        # Older versions of Blender
        prop_id_name = property_group.path_from_id()
        id_data = property_group.id_data
        if prop_id_name in id_data.bl_rna.properties:
            return id_data.bl_rna.properties[prop_id_name].name  # type: ignore

        # Name not found so return id name
        return prop_id_name