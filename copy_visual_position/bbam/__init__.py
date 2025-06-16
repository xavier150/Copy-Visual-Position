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
import importlib

from . import bbam_addon_config
from . import bbam_process
from . import config
from . import manifest_generate
from . import bl_info_generate
from . import addon_file_management
from . import utils
from . import blender_exec
from . import blender_utils

# Reloading modules if they're already loaded
if "bbam_addon_config" in locals():
    importlib.reload(bbam_addon_config)
if "bbam_process" in locals():
    importlib.reload(bbam_process)
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


def install_from_blender(current_only: bool = False):
    # Clear the console before starting the installation process
    os.system('cls' if os.name == 'nt' else 'clear')
    bbam_process.process_install_from_blender(current_only)