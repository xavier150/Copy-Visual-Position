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


def get_tuple_range_version(data):
    """
    Converts version range data into a list of version tuples.

    Parameters:
        data (list): A list of two lists, each representing a version range,
                     e.g., [[1, 0, 0], [2, 0, 0]].

    Returns:
        list: A list of tuples representing the version range,
              e.g., [(1, 0, 0), (2, 0, 0)].
    """
    return [tuple(data[0]), tuple(data[1])]


def get_version_in_range(version, range):
    """
    Checks if a given version is within a specified version range.

    Parameters:
        version (tuple): A tuple representing the current version, e.g., (1, 2, 0).
        range (list): A list of two tuples representing the minimum and maximum versions,
                      e.g., [(1, 0, 0), (2, 0, 0)].

    Returns:
        bool: True if the version is within the specified range; False otherwise.
    """
    min_version, max_version = range
    return min_version <= version <= max_version
