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

import bpy

def print_red(*values):
    print("\033[91m", *values, "\033[0m")

def get_str_version(data):
    """
    Converts a list of version components into a version string.

    Parameters:
        data (list): A list of integers representing the version, e.g., [1, 2, 3].

    Returns:
        str: A string representation of the version, e.g., "1.2.3".
    """
    return f'{data[0]}.{data[1]}.{data[2]}'


def get_should_install(auto_install_range_data):
    min_version = auto_install_range_data[0]
    max_version = auto_install_range_data[1]
    blender_version = bpy.app.version

    if max_version == "LATEST":
        return tuple(min_version) <= blender_version
    else:
        return tuple(min_version) <= blender_version <= tuple(max_version)
    
    return False