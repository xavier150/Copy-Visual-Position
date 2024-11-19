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
#  BBAM -> BleuRaven Blender Addon Manager
#  https://github.com/xavier150/BBAM
#  BleuRaven.fr
#  XavierLoux.com
# ----------------------------------------------

import os
import ast
from . import config
from . import utils

def generate_new_bl_info(addon_generate_config_data, target_build_name):
    """
    Generates a new `bl_info` dictionary for the addon based on the configuration data.

    Parameters:
        addon_generate_config_data (dict): Data containing addon configurations.
        target_build_name (str): The name of the target build configuration.

    Returns:
        dict: A dictionary representing the new `bl_info` for the addon.
    """
    # Check if the target build data exists
    if target_build_name not in addon_generate_config_data["builds"]:
        print(f"Error: Build data for '{target_build_name}' not found!")
        return {}

    manifest_data = addon_generate_config_data["blender_manifest"]
    build_data = addon_generate_config_data["builds"][target_build_name]

    # Populate `bl_info` with addon details
    data = {
        'name': manifest_data["name"],
        'author': manifest_data["maintainer"],
        'version': tuple(manifest_data["version"]),
        'blender': tuple(build_data["blender_version_min"]),
        'location': 'View3D > UI > Unreal Engine',
        'description': manifest_data["tagline"],
        'warning': '',
        "wiki_url": manifest_data["website_url"],
        'tracker_url': manifest_data["report_issue_url"],
        'support': manifest_data["support"],
        'category': manifest_data["category"]
    }

    return data

def format_bl_info_lines(data):
    # Format the new `bl_info` dictionary with line breaks and indentation
    new_bl_info_lines = ["bl_info = {"]
    items = list(data.items())
    for i, (key, value) in enumerate(items):
        if i < len(items) - 1:
            new_bl_info_lines.append(f"    '{key}': {repr(value)},")
        else:
            new_bl_info_lines.append(f"    '{key}': {repr(value)}")
    new_bl_info_lines.append("}\n")  # Close `bl_info` and add an extra line break for readability
    return new_bl_info_lines

def update_file_bl_info(addon_path, data, show_debug=False):
    """
    Updates the `bl_info` dictionary in the addon's __init__.py file with new data.

    Parameters:
        addon_path (str): Path to the addon's root folder.
        data (dict): New `bl_info` dictionary to update in the file.
        show_debug (bool): If True, displays debug information about the update process.
    """
    addon_init_file_path = os.path.join(addon_path, "__init__.py")

    result = replace_file_bl_info(addon_init_file_path, data)
    if result is False:
        result = add_new_bl_info(addon_init_file_path, data)

    if result is False:
        utils.print_red(f"Failed to replace or add bl_info! File: {addon_init_file_path}")
    
    if search_file_bl_info(addon_init_file_path):
        if show_debug:
            print(f"Addon bl_info successfully updated at: {addon_init_file_path}")
            return
    else:
        utils.print_red(f"Failed to found bl_info after update!: {addon_init_file_path}")



def search_file_bl_info(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        tree = ast.parse(content)

    # Locate existing `bl_info` definition
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(target.id == "bl_info" for target in node.targets):
            return True
    return False

def replace_file_bl_info(file_path, data):
    with open(file_path, "r") as file:
        content = file.read()
        tree = ast.parse(content)

    # Locate existing `bl_info` definition
    start_bl_info = None
    end_bl_info = None
    for index, node in enumerate(tree.body):
        if isinstance(node, ast.Assign) and any(target.id == "bl_info" for target in node.targets):
            start_bl_info = node.lineno - 1  # Start line of `bl_info`
            end_bl_info = node.end_lineno  # End line of `bl_info`
            break

    if start_bl_info is not None and end_bl_info is not None:
        lines = content.splitlines()
        # Remove the existing `bl_info` block
        del lines[start_bl_info:end_bl_info]
        # Insert the new `bl_info` block at the same position
        new_bl_info_lines = format_bl_info_lines(data)
        lines[start_bl_info:start_bl_info] = new_bl_info_lines

        # Write the updated content back to the file
        with open(file_path, "w") as file:
            file.write("\n".join(lines))
        return True
    return False

def add_new_bl_info(file_path, data):
    with open(file_path, "r") as file:
        content = file.read()
        tree = ast.parse(content)

    # Find the line number of the `register` function
    index_register = None
    for index, node in enumerate(tree.body):
        if isinstance(node, ast.FunctionDef) and node.name == "register":
            index_register = node.lineno - 1  # `lineno` starts at 1, so we subtract 1 for zero-based index
            break

    lines = content.splitlines()
    new_bl_info_lines = format_bl_info_lines(data)

    if index_register is not None:
        # Insert `bl_info` lines before the `register` function
        for i, line in enumerate(new_bl_info_lines):
            lines.insert(index_register + i, line)
    else:
        # If `register` is not found, append `bl_info` at the end
        lines.extend(new_bl_info_lines)

    # Write the updated content back to the file
    with open(file_path, "w") as file:
        file.write("\n".join(lines))
    return True