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
from . import utils

def uninstall_addon_from_blender(bpy, pkg_id, module):
    """
    Uninstalls an addon from Blender, using the correct method based on Blender's version.

    Parameters:
        bpy (module): Blender's Python API module.
        pkg_id (str): Package ID for the extension (used in newer Blender versions).
        module (str): Name of the addon module to uninstall.
    """
    # For Blender version 4.2.0 and above, use `package_uninstall`
    if bpy.app.version >= (4, 2, 0):
        print(f"Uninstalling extension '{pkg_id}'...")
        bpy.ops.extensions.package_uninstall(repo_index=1, pkg_id=pkg_id)
        bpy.ops.preferences.addon_remove(module=module)
    else:
        # For earlier versions, directly remove the addon using `addon_remove`
        print(f"Uninstalling add-on '{module}'...")
        bpy.ops.preferences.addon_remove(module=module)

def install_zip_addon_from_blender(bpy, zip_file, module):
    """
    Installs a ZIP addon file in Blender, using the correct method based on Blender's version.

    Parameters:
        bpy (module): Blender's Python API module.
        zip_file (str): Path to the ZIP file containing the addon.
        module (str): Name of the addon module to enable after installation.
    """
    if bpy.app.version >= (4, 2, 0):
        # For Blender version 4.2.0 and above, install as an extension
        print("Installing as extension...", zip_file)
        try:
            bpy.ops.extensions.package_install_files(repo="user_default", filepath=zip_file, enable_on_install=True)
            print("Extension installation complete.")
        except Exception as e:
            utils.print_red("An error occurred during installation:", str(e))
    else:
        # For earlier versions, install and enable as an addon
        print("Installing as add-on...", zip_file)
        try:
            bpy.ops.preferences.addon_install(overwrite=True, filepath=zip_file)
            bpy.ops.preferences.addon_enable(module=module)
            print("Add-on installation complete.")
        except Exception as e:
            utils.print_red("An error occurred during installation:", str(e))