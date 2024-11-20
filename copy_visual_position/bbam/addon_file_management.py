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

import shutil
import tempfile
import sys
import os
from . import manifest_generate
from . import bl_info_generate
from . import config
from . import utils
from . import blender_exec
from . import blender_utils


def copy_addon_folder(src, dst, exclude_paths=[], include_paths=[]):
    """
    Copies the addon folder from 'src' to 'dst' while excluding specified files and folders.

    Parameters:
        src (str): Source path of the addon.
        dst (str): Destination path for the copied addon.
        exclude_paths (list): List of file or folder paths to exclude during the copy process.
    """
    # Normalize paths for comparison
    exclude_paths = [os.path.normpath(path) for path in exclude_paths]
    include_paths = [os.path.normpath(path) for path in include_paths]

    # Ignore function to exclude specific files/folders during the copy
    def ignore_files(dir, files):
        ignore_list = []
        for file in files:
            file_path = os.path.join(dir, file)
            relative_path = os.path.normpath(os.path.relpath(file_path, src))

            # Skip directories if only files should be ignored
            if os.path.isdir(file_path):
                continue

            # Check if the file path should be included
            if any(relative_path.startswith(os.path.normpath(path)) for path in include_paths):
                continue  # Skip excluding this file or folder

            # Check if the file path should be excluded
            if any(relative_path.startswith(os.path.normpath(path)) for path in exclude_paths):
                ignore_list.append(file)
        return set(ignore_list)

    shutil.copytree(src, dst, ignore=ignore_files)


def create_temp_addon_folder(addon_path, addon_manifest_data, target_build_name, show_debug=True):
    """
    Creates a temporary folder for the addon, copies relevant files, and generates the manifest.

    Parameters:
        addon_path (str): Root path of the addon.
        addon_manifest_data (dict): Manifest data containing build specifications.
        target_build_name (str): Name of the target build configuration.
        show_debug (bool): If True, debug information is displayed.

    Returns:
        str: Path to the temporary addon folder.
    """
    build_data = addon_manifest_data["builds"][target_build_name]
    generate_method = build_data["generate_method"]

    # Step 1: Create a temporary directory for the addon
    temp_dir = tempfile.mkdtemp(prefix="blender_addon_")
    temp_addon_path = os.path.join(temp_dir, os.path.basename(addon_path))

    # Step 2: Copy addon folder to temporary directory, excluding specified paths
    exclude_paths = build_data.get("exclude_paths", [])
    include_paths = build_data.get("include_paths", [])
    exclude_paths.append("bbam/")  # Exclude addon manager from the final build
    copy_addon_folder(addon_path, temp_addon_path, exclude_paths, include_paths)
    print(f"Copied build '{target_build_name}' to temporary location: {temp_addon_path}")

    # Step 3: Generate addon manifest based on generation method
    if generate_method == "EXTENTION_COMMAND":
        new_manifest = manifest_generate.generate_new_manifest(addon_manifest_data, target_build_name)
        manifest_generate.save_addon_manifest(temp_addon_path, new_manifest, show_debug)
    elif generate_method == "SIMPLE_ZIP":
        new_manifest = bl_info_generate.generate_new_bl_info(addon_manifest_data, target_build_name)
        bl_info_generate.update_file_bl_info(temp_addon_path, new_manifest, show_debug)

    return temp_addon_path

def get_zip_output_filename(addon_path, addon_manifest_data, target_build_name):
    """
    Generates the output filename for the ZIP file based on naming conventions in the manifest.

    Parameters:
        addon_path (str): Root path of the addon.
        addon_manifest_data (dict): Manifest data containing build specifications.
        target_build_name (str): Name of the target build configuration.

    Returns:
        str: Full path of the output ZIP file.
    """
    manifest_data = addon_manifest_data["blender_manifest"]
    build_data = addon_manifest_data["builds"][target_build_name]
    version = utils.get_str_version(manifest_data["version"])

    # Formatting output filename
    output_folder_path = os.path.abspath(os.path.join(addon_path, '..', config.build_output_folder))
    formatted_file_name = build_data["naming"].replace("{Name}", build_data["pkg_id"]).replace("{Version}", version)
    output_filepath = os.path.join(output_folder_path, formatted_file_name)
    return output_filepath

def zip_addon_folder(src, addon_path, addon_manifest_data, target_build_name, blender_executable_path):
    """
    Creates a ZIP archive of the addon folder, either through Blender's extension command
    or by using a simple ZIP method.

    Parameters:
        src (str): Path to the source addon folder.
        addon_path (str): Root path of the addon.
        addon_manifest_data (dict): Manifest data containing build specifications.
        target_build_name (str): Name of the target build configuration.
        blender_executable_path (str): Path to the Blender executable for running commands.

    Returns:
        str: Path to the created ZIP file.
    """
    build_data = addon_manifest_data["builds"][target_build_name]
    generate_method = build_data["generate_method"]

    # Define output file path and ensure the output directory exists
    output_filepath = get_zip_output_filename(addon_path, addon_manifest_data, target_build_name)
    output_dir = os.path.dirname(output_filepath)
    os.makedirs(output_dir, exist_ok=True)

    # Run addon zip process based on the specified generation method
    if generate_method == "EXTENTION_COMMAND":
        print("Start build with extension command")
        result = blender_exec.build_extension(src, output_filepath, blender_executable_path)
        print(result.stdout)
        print(result.stderr, file=sys.stderr)

        created_filename = blender_exec.get_build_file(result)
        if created_filename:
            print("Start Validate")
            blender_exec.validate_extension(created_filename, blender_executable_path)
            print("End Validate")

        return created_filename
    
    elif generate_method == "SIMPLE_ZIP":
        print("Start creating simple ZIP file with root folder using shutil")

        # Specify the root folder name inside the ZIP file
        root_folder_name = build_data["module"]

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy the source folder to a temporary root folder
            temp_root = os.path.join(temp_dir, root_folder_name)
            shutil.copytree(src, temp_root)

            # Use shutil to create the ZIP archive from the temporary directory
            base_name = os.path.splitext(output_filepath)[0]  # Path without .zip extension
            shutil.make_archive(base_name, 'zip', temp_dir, root_folder_name)
        
        print(f"SIMPLE_ZIP created successfully at {output_filepath}")
        return output_filepath