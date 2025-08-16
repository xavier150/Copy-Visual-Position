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
import bpy
from typing import Optional
from ... import __package__ as base_package  # type: ignore

def get_package_version(pkg_idname: Optional[str] = None, repo_module: str = 'user_default') -> Optional[str]:
    if bpy.app.version < (4, 2, 0):
        print("Blender extensions are not supported under 4.2. Please use bbpl.blender_addon.addon_utils instead.")
        return None
    
    manifest_filename = "blender_manifest.toml"
    
    if pkg_idname:
        file_path = os.path.join(bpy.utils.user_resource('EXTENSIONS'), repo_module, pkg_idname, manifest_filename)
    else:
        from addon_utils import _extension_module_name_decompose  # type: ignore
        repo_module, pkg_idname = _extension_module_name_decompose(base_package)  # type: ignore
        file_path = os.path.join(bpy.utils.user_resource('EXTENSIONS'), repo_module, pkg_idname, manifest_filename)  # type: ignore
    
    version = None
    if os.path.isfile(file_path):  # type: ignore
        with open(file_path, 'r') as file:  # type: ignore
            for line in file:
                if line.startswith("version"):
                    version = line.split('=')[1].strip().strip('"')
                    break
    else:
        print(f"File {file_path} does not exist.")
    
    return version

def get_package_path(pkg_idname: Optional[str] = None, repo_module: str = 'user_default') -> Optional[str]:
    if bpy.app.version < (4, 2, 0):
        print("Blender extensions are not supported under 4.2. Please use bbpl.blender_addon.addon_utils instead.")
        return None

    if pkg_idname:
        return os.path.join(bpy.utils.user_resource('EXTENSIONS'), repo_module, pkg_idname)
    else:
        from addon_utils import _extension_module_name_decompose  # type: ignore
        repo_module, pkg_idname = _extension_module_name_decompose(base_package)  # type: ignore
        return os.path.join(bpy.utils.user_resource('EXTENSIONS'), repo_module, pkg_idname)  # type: ignore

