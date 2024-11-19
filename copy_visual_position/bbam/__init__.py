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
import json
import importlib

from . import config
from . import manifest_generate
from . import bl_info_generate
from . import addon_file_management
from . import utils
from . import blender_exec
from . import blender_utils

# Reloading modules if they're already loaded
if "config" in locals():
    importlib.reload(config)
if "manifest_generate" in locals():
    importlib.reload(manifest_generate)
if "bl_info_generate" in locals():
    importlib.reload(bl_info_generate)
if "addon_file_management" in locals():
    importlib.reload(addon_file_management)
if "utils" in locals():
    importlib.reload(utils)
if "blender_exec" in locals():
    importlib.reload(blender_exec)
if "blender_utils" in locals():
    importlib.reload(blender_utils)

def install_from_blender():
    """
    Loads the addon's configuration file to retrieve its manifest data and initiates
    the installation process within Blender.
    """
    # Get the path of the current addon's configuration file from `config`
    addon_manifest = config.addon_generate_config

    # Construct absolute paths for addon and manifest file
    addon_path = os.path.abspath(os.path.join(__file__, '..', '..'))
    search_addon_folder = os.path.abspath(os.path.join(addon_path, addon_manifest))

    # Load the manifest file data if it exists
    if os.path.isfile(search_addon_folder):
        with open(search_addon_folder, 'r', encoding='utf-8') as file:
            data = json.load(file)
            install_from_blender_with_build_data(addon_path, data)
    else:
        print(f"Error: '{addon_manifest}' was not found in '{search_addon_folder}'.")

def install_from_blender_with_build_data(addon_path, addon_manifest_data):
    """
    Manages the addon installation in Blender based on the build data from the manifest.

    Parameters:
        addon_path (str): The path to the addon's root directory.
        addon_manifest_data (dict): The data structure containing build specifications.
    """
    # Import bpy lib here when exec from Blender.
    import bpy

    # Get Blender executable path from bpy
    blender_executable_path = bpy.app.binary_path

    # Process each build specified in the manifest data
    for target_build_name in addon_manifest_data["builds"]:
        # Create temporary addon folder
        temp_addon_path = addon_file_management.create_temp_addon_folder(
            addon_path, addon_manifest_data, target_build_name, config.show_debug
        )
        # Zip the addon folder for installation
        zip_file = addon_file_management.zip_addon_folder(
            temp_addon_path, addon_path, addon_manifest_data, target_build_name, blender_executable_path
        )
        
        build_data = addon_manifest_data["builds"][target_build_name]
        pkg_id = build_data.get("pkg_id")
        module = build_data.get("module")

        # Check if the addon should be installed based on Blender's version
        auto_install_range = utils.get_tuple_range_version(build_data.get("auto_install_range"))
        should_install = utils.get_version_in_range(bpy.app.version, auto_install_range)
        if should_install:

            # Uninstall previous versions if they exist
            blender_utils.uninstall_addon_from_blender(bpy, pkg_id, module)
            blender_utils.install_zip_addon_from_blender(bpy, zip_file, module)